#! /usr/bin/env sh

# prestart.sh

set -e
set -x

echo "Waiting for postgres connection"

while ! nc -z db 5432; do
    sleep 0.1
done

echo "PostgreSQL started"

# Run Database migrations

echo "Running Database Migrations"

alembic upgrade head

echo "Database Migrations complete"

exec "$@"