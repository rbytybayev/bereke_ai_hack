CREATE TABLE sanctions_dow_jones (
    id SERIAL PRIMARY KEY,
    name TEXT,
    risk_type TEXT,
    role TEXT,
    list_name TEXT,
    jurisdiction TEXT,
    source TEXT,
    extra_data JSONB
);