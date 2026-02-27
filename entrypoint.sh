#!/bin/sh
set -e

if [ "${DJANGO_DB_ENGINE}" = "postgres" ]; then
  echo "Waiting for PostgreSQL at ${POSTGRES_HOST}:${POSTGRES_PORT}..."
  python - <<'PY'
import os
import time

import psycopg

host = os.getenv("POSTGRES_HOST", "db")
port = os.getenv("POSTGRES_PORT", "5432")
dbname = os.getenv("POSTGRES_DB", "school_library")
user = os.getenv("POSTGRES_USER", "school_library")
password = os.getenv("POSTGRES_PASSWORD", "school_library")

for attempt in range(1, 31):
    try:
        psycopg.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password,
            connect_timeout=2,
        ).close()
        print("PostgreSQL is ready.")
        break
    except Exception:
        if attempt == 30:
            raise
        time.sleep(1)
PY
fi

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec python manage.py runserver 0.0.0.0:8000
