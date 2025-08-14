#!/bin/bash
set -e

echo "🔄 Esperando que la base de datos esté disponible..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done
echo "✅ Base de datos disponible"

echo "🔄 Ejecutando migraciones..."
python manage.py makemigrations notifications
python manage.py migrate
python manage.py migrate django_celery_beat

echo "🔄 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "🚀 Iniciando servidor..."
exec "$@" 