-- init.sql: Ensure required tables exist

-- Table for Backlog model
CREATE TABLE IF NOT EXISTS etl_backlog (
    id SERIAL PRIMARY KEY,
    link TEXT NOT NULL,
    attempts INTEGER DEFAULT 0
);

-- Table for Clusters (info about clusters) model
CREATE TABLE IF NOT EXISTS etl_clusters (
    id SERIAL PRIMARY KEY,
    link TEXT NOT NULL,
    decade INTEGER,
    gender TEXT,
    curated BOOLEAN,
    cluster INTEGER,
    reduction TEXT,
    clusterization TEXT,
);

-- Table for Perfume model
CREATE TABLE IF NOT EXISTS etl_perfume (
    id SERIAL PRIMARY KEY,
    link TEXT NOT NULL,
    name VARCHAR(255) NOT NULL,
    brand VARCHAR(255) NOT NULL,
    rel_year INTEGER NOT NULL,
    rel_decade INTEGER NOT NULL,
    description TEXT DEFAULT 'No description',
    image TEXT DEFAULT 'No image',
    notes TEXT[] DEFAULT '{}',
    type TEXT[] DEFAULT '{}',
    type_numbers INTEGER[] DEFAULT '{}',
    style TEXT[] DEFAULT '{}',
    style_numbers INTEGER[] DEFAULT '{}',
    season TEXT[] DEFAULT '{}',
    season_numbers INTEGER[] DEFAULT '{}',
    occasion TEXT[] DEFAULT '{}',
    occasion_numbers INTEGER[] DEFAULT '{}',
    scent FLOAT NOT NULL,
    longevity FLOAT NOT NULL,
    sillage FLOAT NOT NULL,
    bottle FLOAT NOT NULL,
    value_for_money FLOAT NOT NULL
);