#!/bin/sh
set -e

# wait for db to be ready (only applies when using Postgres)
if [ "${USE_POSTGRES}" = "true" ]; then
  echo "Waiting for Postgres..."
  max_tries=30
  count=0
  until python -c "import psycopg2; psycopg2.connect(host='$POSTGRES_HOST', user='$POSTGRES_USER', password='$POSTGRES_PASSWORD', database='$POSTGRES_DB')" 2>/dev/null; do
    count=$((count + 1))
    if [ $count -ge $max_tries ]; then
      echo "Failed to connect to Postgres after $max_tries attempts"
      exit 1
    fi
    echo "Postgres not ready, attempt $count of $max_tries..."
    sleep 2
  done
  echo "Postgres is ready!"
fi

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput || true

exec "$@"
