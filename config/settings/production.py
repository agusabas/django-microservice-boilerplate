from .base import *
import environ

# Leer variables de entorno específicas para production
env = environ.Env()
env_file = ROOT_DIR.path('.envs').path(f'.env.{ENVIRONMENT}')
environ.Env.read_env(env_file)

# Configuraciones específicas para production
DEBUG = False

# Configuración de logging para producción
LOGGING['loggers']['celery']['level'] = 'ERROR'
LOGGING['root']['level'] = 'WARNING'

# Configuraciones de seguridad adicionales
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 31536000
SECURE_REDIRECT_EXEMPT = []
# Temporalmente deshabilitado para diagnosticar problemas de routing
# SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_TZ = True

# Configuraciones de sesión más seguras
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
