#!/usr/bin/env bash

# Directory for neo4j instances
instancesDirectory="$HOME/neo4j-instances"

# Ensure this script is not run as root
if [ "$(whoami)" == "root" ]; then
    echo "This script should not be run as root."
    exit 1
fi

# Check if the directory argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <directory-of-neo4j-prompts>"
    exit 1
fi

promptDirectory="$1"

# Function to clear existing databases
function clearExistingDatabases {
    echo "Clearing existing databases..."
    if [ -d "$instancesDirectory/ports" ]; then
        find "$instancesDirectory/ports" -mindepth 1 -type d -exec rm -rf {} +
    fi
}

# Function to create databases and execute prompts
function createAndExecute {
    for file in $promptDirectory/*.txt; do
        if [ ! -f "$file" ]; then
            continue
        fi
        # Extract the database name from the filename
        dbName=$(basename "$file" .txt)

        echo "Creating database for $dbName..."
        ./neo4j-instance.sh create -d "$dbName"

        # Get the last used port for Bolt connection
        lastPort=$(ls "$instancesDirectory/ports" | sort -n | tail -1)
        boltPort=$(cat "$instancesDirectory/ports/$lastPort/bolt-port")

        # Start the database.
        ./neo4j-instance.sh start $lastPort

        echo "Importing data from $file into database on port $boltPort..."
        cat "$file" | $instancesDirectory/ports/$lastPort/bin/cypher-shell -u neo4j -p 11111111 -a "neo4j://localhost:$boltPort" --format plain

        # Stop the database
        # ./neo4j-instance.sh stop $lastPort
    done
}

# Main execution flow
clearExistingDatabases
createAndExecute

echo "All tasks completed successfully."
