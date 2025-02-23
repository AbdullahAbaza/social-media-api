#! /usr/bin/env sh

# prestart.sh

set -e

echo "Starting prestart script..."

# Check if nc (netcat) is installed
if ! command -v nc &> /dev/null; then
    echo "Error: nc (netcat) is not installed. Please install it and try again."
    exit 1
fi

# Parse command-line arguments
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <db_host> <db_port> [command]"
    exit 1
fi

DB_HOST="$1"  # First argument: database host
DB_PORT="$2"  # Second argument: database port
shift 2       # Shift arguments to pass the remaining arguments to exec

# Wait for PostgreSQL to be ready
echo "Checking PostgreSQL connection at $DB_HOST:$DB_PORT..."

timeout=30
while ! nc -z "$DB_HOST" "$DB_PORT"; do
    sleep 0.1
    timeout=$((timeout - 1))
    if [ $timeout -le 0 ]; then
        echo "Timeout waiting for PostgreSQL at $DB_HOST:$DB_PORT"
        exit 1
    fi
done

echo "PostgreSQL started at $DB_HOST:$DB_PORT"

# Run Database migrations
echo "Running Database Migrations"

# Capture the output and exit code of the migration command
if ! output=$(alembic upgrade head 2>&1); then
    echo "Error: Database migrations failed. See the error below:"
    echo "$output"  # Print the captured output (error message)
    exit 1
fi

echo "Database Migrations complete"

# Execute the main command (remaining arguments)
exec "$@"