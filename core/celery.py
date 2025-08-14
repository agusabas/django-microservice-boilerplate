from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from datetime import datetime
import pytz

# Configurar el módulo de settings según el ambiente
environment = os.getenv('ENVIRONMENT', 'local')
settings_module = f'config.settings.{environment}'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

app = Celery('django_microservice')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Configurar zona horaria para Buenos Aires
app.conf.timezone = 'America/Argentina/Buenos_Aires'
app.conf.enable_utc = False

# Configuración de tareas periódicas
app.conf.beat_schedule = {
    # Add your periodic tasks here
    # 'your-periodic-task': {
    #     'task': 'apps.your_app.tasks.your_task',
    #     'schedule': crontab(minute='*/5'),
    #     'options': {
    #         'queue': 'default',
    #     }
    # },
}

# Resto de la configuración existente
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='America/Argentina/Buenos_Aires',
    enable_utc=False,
    
    task_routes={
        # Add your task routes here
        # 'apps.your_app.tasks.your_task': {'queue': 'default'},
    },
    
    task_soft_time_limit=300,
    task_time_limit=600,
    task_rate_limit='100/m',
)

app.conf.task_queues = {
    'default': {
        'exchange': 'default',
        'routing_key': 'default',
    },
    'bulk': {
        'exchange': 'bulk',
        'routing_key': 'bulk',
    },
    'scheduled': {
        'exchange': 'scheduled',
        'routing_key': 'scheduled',
    }
}

app.conf.task_default_queue = 'default'
app.conf.task_default_exchange = 'default'
app.conf.task_default_routing_key = 'default'

app.autodiscover_tasks()

# Configuración adicional para manejo de errores
app.conf.broker_transport_options = {
    'visibility_timeout': 3600,  # 1 hora
    'socket_timeout': 30,        # 30 segundos
    'socket_connect_timeout': 30,
}

app.conf.broker_connection_retry_on_startup = True
app.conf.broker_connection_max_retries = 10 