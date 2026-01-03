
#!/bin/bash
set -e

# Function to create user and database
create_db() {
    local dbname=$1
    echo "Creating database: $dbname"
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
        SELECT 'CREATE DATABASE $dbname'
        WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$dbname')\gexec
EOSQL
}

# Create databases for God Mode instances
create_db "radarr_en"
create_db "radarr_es"
create_db "radarr_it"
create_db "sonarr_en"
create_db "sonarr_es"
create_db "sonarr_it"
# Prowlarr DB is already default or created via its own vars, but good to have explicit
create_db "prowlarr"
