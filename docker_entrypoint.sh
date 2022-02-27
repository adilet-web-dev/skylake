#!/usr/bin bash

echo -e "Wait for database\n"
POSTGRES_TCP=$(echo "$DATABASE_URL" | sed 's/^postgres/tcp/')
dockerize -wait "$POSTGRES_TCP" -timeout 20s


echo -e "Collecting static assets\n"
python manage.py collectstatic --noinput --verbosity 0

echo -e "Migrating database\n"
python manage.py migrate

echo -e "Starting server\n"

daphne -p 8000 -b 0.0.0.0 config.asgi:application
