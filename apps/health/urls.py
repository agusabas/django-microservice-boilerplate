from django.urls import path
from .views import HealthCheckView, DetailedHealthCheckView

urlpatterns = [
    path('', HealthCheckView.as_view(), name='health-check'),
    path('detailed/', DetailedHealthCheckView.as_view(), name='detailed-health-check'),
]