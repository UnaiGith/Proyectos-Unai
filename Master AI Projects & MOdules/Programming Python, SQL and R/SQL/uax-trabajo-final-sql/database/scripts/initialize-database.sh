#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Only run the SQL scripts that recreate and initialize the database if the environment variable is set to true
if [ "$RECREATE_DATABASE_WITH_INITIAL_TEST_DATA" = "true" ]; then
    echo "💭 Recreating and initializing the database..."

    DATA_FOLDER_PATH="/database/data"
    DATABASE_FILE_PATH="$DATA_FOLDER_PATH/database.db"

    # Remove all inside the data folder except .gitkeep (this removes cached data from sqlitebrowser)
    echo "💭 Removing cached data from sqlitebrowser..."
    find $DATA_FOLDER_PATH -mindepth 1 ! -name '.gitkeep' -exec rm -rf {} +
  
    # Execute the SQL scripts over the database
    sqlite3 $DATABASE_FILE_PATH < /database/scripts/ddl/create.sql
    sqlite3 $DATABASE_FILE_PATH < /database/scripts/dml/insert.sql
  
    echo "✅ Database recreated and initialized successfully"
else
    echo "⏩ Skipped execution of scripts that recreate and initialize the database"
fi

# Keep the connection to the database alive
echo "🚀 Database container is running..."
tail -f /dev/null
