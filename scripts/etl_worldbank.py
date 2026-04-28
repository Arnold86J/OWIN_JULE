import pandas as pd
import numpy as np
import os
import asyncio
from sqlalchemy import create_engine, text

# Import cache invalidation if available
try:
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from api.cache import clear_cache
except ImportError:
    clear_cache = None

def load_data(filepath):
    """Loads World Bank CSV data."""
    return pd.read_csv(filepath)

def melt_data(df):
    """Transforms wide format (years as columns) to long format."""
    id_vars = ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code']
    # Filter columns that are years (assuming they are 4-digit strings)
    year_cols = [col for col in df.columns if col.isdigit() and len(col) == 4]

    df_long = pd.melt(
        df,
        id_vars=id_vars,
        value_vars=year_cols,
        var_name='year',
        value_name='value'
    )
    df_long['year'] = df_long['year'].astype(int)
    return df_long

def clean_data(df):
    """Handles missing values with interpolation and forward/backward fill."""
    # Ensure data is sorted for interpolation
    df = df.sort_values(by=['Country Code', 'Indicator Code', 'year'])

    def process_group(group):
        # Linear interpolation for internal gaps
        group['value'] = group['value'].interpolate(method='linear')
        # Forward and backward fill for edges, limited to 3 years
        group['value'] = group['value'].ffill(limit=3)
        group['value'] = group['value'].bfill(limit=3)
        return group

    # Apply processing per group
    # Using group_keys=True to keep them in index, then we'll reset carefully
    df = df.groupby(['Country Code', 'Indicator Code'], group_keys=True).apply(process_group)

    # Drop rows where value is still NaN after filling
    df = df.dropna(subset=['value'])

    return df

def map_to_schema(df):
    """Rename columns to match SQL schema conventions."""
    # Reset index to bring Country Code and Indicator Code back from MultiIndex
    df = df.reset_index(drop=False)

    mapping = {
        'Country Code': 'iso_code',
        'Indicator Code': 'indicator_code',
        'year': 'year',
        'value': 'value'
    }
    # Only keep mapping keys that exist in columns
    existing_keys = [k for k in mapping.keys() if k in df.columns]
    return df[existing_keys].rename(columns=mapping)

def save_to_csv(df, output_path):
    """Saves the cleaned dataframe to CSV."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to {output_path}")

def load_to_postgres(df, raw_df, db_url):
    """Loads data into PostgreSQL, resolving dimensions and foreign keys."""
    try:
        engine = create_engine(db_url)

        # 1. Upsert Countries
        countries_df = raw_df[['Country Code', 'Country Name']].drop_duplicates()
        countries_df.columns = ['iso_code', 'full_name']
        countries_df.to_sql('countries_staging', engine, if_exists='replace', index=False)
        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO countries (iso_code, full_name)
                SELECT iso_code, full_name FROM countries_staging
                ON CONFLICT (iso_code) DO UPDATE SET full_name = EXCLUDED.full_name
            """))

        # 2. Upsert Indicators
        indicators_df = raw_df[['Indicator Code', 'Indicator Name']].drop_duplicates()
        indicators_df.columns = ['code', 'name']
        indicators_df.to_sql('indicators_staging', engine, if_exists='replace', index=False)
        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO indicators (code, name)
                SELECT code, name FROM indicators_staging
                ON CONFLICT (code) DO UPDATE SET name = EXCLUDED.name
            """))

        # 3. Resolve IDs and Load Data Points
        # Load ID mappings
        with engine.connect() as conn:
            countries_map = pd.read_sql("SELECT id, iso_code FROM countries", conn)
            indicators_map = pd.read_sql("SELECT id, code FROM indicators", conn)

        df = df.merge(countries_map, left_on='iso_code', right_on='iso_code')
        df = df.rename(columns={'id': 'country_id'})

        df = df.merge(indicators_map, left_on='indicator_code', right_on='code')
        df = df.rename(columns={'id': 'indicator_id'})

        final_data = df[['country_id', 'indicator_id', 'year', 'value']]
        final_data.to_sql('data_points_staging', engine, if_exists='replace', index=False)

        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO data_points (country_id, indicator_id, year, value)
                SELECT country_id, indicator_id, year, value FROM data_points_staging
                ON CONFLICT (country_id, indicator_id, year) DO UPDATE SET value = EXCLUDED.value
            """))

        print("Data successfully loaded into production tables.")
    except Exception as e:
        print(f"Error loading to Postgres: {e}")

if __name__ == "__main__":
    input_file = "data/raw/world_bank_data.csv"
    output_file = "data/processed/cleaned_indicators.csv"

    print("Starting ETL process...")

    # 1. Load
    raw_df = load_data(input_file)

    # 2. Transform (Melt)
    long_df = melt_data(raw_df)

    # 3. Clean (Interpolate/Fill)
    cleaned_df = clean_data(long_df)

    # 4. Map
    final_df = map_to_schema(cleaned_df)

    # 5. Save
    save_to_csv(final_df, output_file)

    # 6. Database Load (Optional - enabled if DATABASE_URL is present)
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        load_to_postgres(final_df, raw_df, db_url)

    # 7. Clear Cache (Optional - enabled if Redis is used)
    if clear_cache:
        try:
            asyncio.run(clear_cache())
        except Exception as e:
            print(f"Could not clear cache: {e}")

    print("ETL process completed.")
