import time
import logging
from django.db import connection
from django.core.cache import cache
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

logger = logging.getLogger(__name__)


class HealthCheckView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        """
        Simple health check endpoint for monitoring and load balancers
        """
        logger.info("HealthCheckView received request")
        try:
            health_data = {
                'status': 'healthy',
                'service': 'django-microservice',
                'version': '1.0.0',
                'timestamp': int(time.time())
            }
            
            logger.info("Health check completed successfully")
            return Response(health_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error in health check: {str(e)}", exc_info=True)
            return Response(
                {'error': 'Health check failed', 'message': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DetailedHealthCheckView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        """
        Detailed health check with database and cache connectivity
        """
        logger.info("DetailedHealthCheckView received request")
        try:
            health_data = {
                'status': 'healthy',
                'service': 'django-microservice',
                'version': '1.0.0',
                'timestamp': int(time.time()),
                'checks': {
                    'database': self._check_database(),
                    'cache': self._check_cache(),
                }
            }
            
            # Determine overall status
            all_healthy = all(
                check_result['status'] == 'healthy' 
                for check_result in health_data['checks'].values()
            )
            
            if not all_healthy:
                health_data['status'] = 'unhealthy'
                logger.warning(f"Detailed health check failed: {health_data}")
                return Response(health_data, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            
            logger.info("Detailed health check completed successfully")
            return Response(health_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error in detailed health check: {str(e)}", exc_info=True)
            return Response(
                {'error': 'Detailed health check failed', 'message': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _check_database(self):
        """Check database connectivity"""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            logger.debug("Database connection check successful")
            return {
                'status': 'healthy',
                'message': 'Database connection successful'
            }
        except Exception as e:
            logger.error(f"Database connection check failed: {str(e)}")
            return {
                'status': 'unhealthy',
                'message': f'Database connection failed: {str(e)}'
            }
    
    def _check_cache(self):
        """Check Redis cache connectivity"""
        try:
            # Try to set and get a test value
            test_key = 'health_check_test'
            test_value = 'ok'
            cache.set(test_key, test_value, 30)  # 30 seconds TTL
            retrieved_value = cache.get(test_key)
            
            if retrieved_value == test_value:
                cache.delete(test_key)  # Clean up
                logger.debug("Cache connection check successful")
                return {
                    'status': 'healthy',
                    'message': 'Cache connection successful'
                }
            else:
                logger.error("Cache set/get test failed - value mismatch")
                return {
                    'status': 'unhealthy',
                    'message': 'Cache set/get test failed'
                }
        except Exception as e:
            logger.error(f"Cache connection check failed: {str(e)}")
            return {
                'status': 'unhealthy',
                'message': f'Cache connection failed: {str(e)}'
            }