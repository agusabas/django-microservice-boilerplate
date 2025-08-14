# Django Microservice Boilerplate

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/django-4.2-green.svg)](https://djangoproject.com)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A production-ready Django microservice boilerplate with multi-environment configuration, async task processing, and comprehensive observability.

## Features

- **Multi-Environment Configuration** - Separate settings for local, QA, and production
- **Async Task Processing** - Celery with Redis broker for background jobs
- **Real-time Communication** - WebSocket support via Django Channels
- **Health Monitoring** - Built-in health checks with database and cache validation
- **Observability** - Prometheus metrics and structured logging
- **Production Ready** - Security headers, SSL termination, and performance optimizations
- **Container Support** - Multi-stage Docker builds and docker-compose configurations

## Quick Start

### Prerequisites

- Python 3.9+
- Docker & Docker Compose
- Redis
- PostgreSQL

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/agusabas/django-microservice-boilerplate.git
   cd django-microservice-boilerplate
   ```

2. **Set up environment variables**

   ```bash
   cp .envs/.env.local.example .envs/.env.local
   # Edit .envs/.env.local with your configuration
   ```

3. **Start with Docker**

   ```bash
   export ENVIRONMENT=local
   docker compose -f local.yaml up --build
   ```

4. **Or run locally**
   ```bash
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

The service will be available at `http://localhost:8000`

## Usage

### Health Checks

- `GET /health/` - Basic health status
- `GET /health/detailed/` - Detailed health with dependency checks

### Admin Interface

- `GET /admin/` - Django admin interface

### Metrics

- `GET /prometheus/` - Prometheus metrics endpoint

## Configuration

### Environment Variables

Configuration is managed through environment-specific files in `.envs/`:

- `.env.local` - Development settings
- `.env.production` - Production settings
- `.env.qa` - QA/Testing settings

Key variables:

```env
SECRET_KEY=your-secret-key
DEBUG=True/False
POSTGRES_HOST=db
POSTGRES_DB=your_database
REDIS_HOST=redis
CELERY_BROKER_URL=redis://redis:6379/0
```

### Adding New Apps

1. Create the Django app:

   ```bash
   python manage.py startapp your_app apps/your_app
   ```

2. Register in `config/settings/base.py`:

   ```python
   PROJECT_APPS = [
       'apps.health',
       'apps.your_app',  # Add here
   ]
   ```

3. Add URLs in `core/urls.py`:
   ```python
   urlpatterns = [
       path('api/your-app/', include('apps.your_app.urls')),
   ]
   ```

## Development

### Running Tests

```bash
python manage.py test
```

### Running Celery

```bash
# Worker
celery -A core worker -l DEBUG

# Beat scheduler
celery -A core beat -l DEBUG
```

## Deployment

### Docker

```bash
# Production
docker compose -f production.yaml up --build

# QA
docker compose -f qa.yaml up --build
```

### Environment-specific Features

- **Local**: Debug enabled, detailed logging
- **QA**: Production-like with test data
- **Production**: SSL, security headers, optimized for performance

## Project Structure

```
├── apps/                    # Django applications
│   └── health/             # Health check endpoints
├── config/
│   └── settings/           # Environment-specific settings
├── core/                   # Django core configuration
├── docker/                 # Dockerfiles for each environment
├── .envs/                  # Environment variable templates
└── requirements.txt        # Python dependencies
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Made with ❤️ for the Django community**
