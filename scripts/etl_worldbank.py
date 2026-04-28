import pandas as pd
import numpy as np
import os
from sqlalchemy import create_engine

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

def load_to_postgres(df, db_url):
    """Optional: Loads data into PostgreSQL."""
    try:
        engine = create_engine(db_url)
        # Note: In a real scenario, we'd need to map iso_code/indicator_code
        # to their respective IDs in the database.
        # This implementation assumes table names and structure match for simplicity
        # or requires a staging table approach.
        df.to_sql('staging_data_points', engine, if_exists='replace', index=False)
        print("Data successfully loaded to staging_data_points table.")
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
        load_to_postgres(final_df, db_url)

    print("ETL process completed.")
