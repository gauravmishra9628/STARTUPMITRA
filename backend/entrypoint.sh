#!/bin/sh
set -e

# wait for db to be ready (only applies when using Postgres)
if [ "${USE_POSTGRES}" = "true" ]; then
  echo "Waiting for Postgres..."
  until pg_isready -h "$POSTGRES_HOST" -U "$POSTGRES_USER"; do
    sleep 1
  done
fi

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput || true

exec "$@"
