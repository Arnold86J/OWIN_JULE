-- Drop tables if they exist to allow for clean re-runs
DROP TABLE IF EXISTS data_points;
DROP TABLE IF EXISTS indicators;
DROP TABLE IF EXISTS countries;

-- Countries table
CREATE TABLE countries (
    id SERIAL PRIMARY KEY,
    iso_code VARCHAR(3) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    region VARCHAR(100),
    sub_region VARCHAR(100),
    income_level VARCHAR(100)
);

-- Indicators table
CREATE TABLE indicators (
    id SERIAL PRIMARY KEY,
    code VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    unit VARCHAR(50),
    description TEXT
);

-- Data points table
CREATE TABLE data_points (
    id SERIAL PRIMARY KEY,
    country_id INTEGER REFERENCES countries(id) ON DELETE CASCADE,
    indicator_id INTEGER REFERENCES indicators(id) ON DELETE CASCADE,
    year INTEGER NOT NULL,
    value NUMERIC NOT NULL,
    CONSTRAINT uq_country_indicator_year UNIQUE (country_id, indicator_id, year)
);

-- Indexes for optimization
CREATE INDEX idx_data_points_year ON data_points(year);
CREATE INDEX idx_data_points_country_id ON data_points(country_id);
CREATE INDEX idx_data_points_indicator_id ON data_points(indicator_id);
