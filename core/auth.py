import jwt
from django.conf import settings
from datetime import datetime
from rest_framework.exceptions import AuthenticationFailed
from functools import wraps
from rest_framework.response import Response
from rest_framework import status
import requests
import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def generate_service_token(secret):
    """
    Genera un token JWT para que el servicio de notificaciones 
    se comunique con el monolito
    """
    payload = {
        'iss': 'notifications_service',
        'aud': 'monolith',
        'iat': datetime.utcnow(),
        'type': 'service',
        'service_id': 'notifications'
    }

    token = jwt.encode(
        payload,
        secret,
        algorithm='HS256'
    )

    return token

def verify_jwt_token(token):
    try:
        payload = jwt.decode(token, settings.SERVICES_JWT_SECRET, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('El token ha expirado')
    except jwt.InvalidTokenError:
        raise AuthenticationFailed('Token inválido')
    

def admin_required():
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(view_instance, request, *args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return Response(
                    {"error": "Token no proporcionado"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            try:
                # Extraer el token
                prefix, token = auth_header.split(' ')
                if prefix not in ['JWT', 'Bearer']:
                    return Response(
                        {"error": "Formato de token inválido"},
                        status=status.HTTP_401_UNAUTHORIZED
                    )

                # Primero verificamos el token localmente
                try:
                    payload = verify_jwt_token(token)
                    logger.info(f"Token verificado localmente: {payload}")
                except AuthenticationFailed as e:
                    return Response(
                        {"error": str(e)},
                        status=status.HTTP_401_UNAUTHORIZED
                    )

                # Si el token es válido, verificamos el rol con el servicio de autenticación
                response = requests.get(
                    f"{os.getenv('AUTH_SERVICE_HOST')}/auth/users/me/",
                    headers={"Authorization": f"JWT {token}"}
                )
                response.raise_for_status()
                
                user_details = response.json()
                logger.info(f"User details: {user_details}")

                if user_details.get('role') != 'ADMIN':
                    return Response(
                        {"error": "No tienes rol para realizar esta acción"},
                        status=status.HTTP_403_FORBIDDEN
                    )

                # Si todo está bien, continuar con la vista
                return view_func(view_instance, request, *args, **kwargs)

            except requests.exceptions.RequestException as e:
                logger.error(f"Error al contactar el servicio de autenticación: {str(e)}")
                return Response(
                    {"error": "Error al contactar el servicio de autenticación"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            except Exception as e:
                logger.error(f"Error inesperado: {str(e)}")
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return _wrapped_view
    return decorator


def user_required():
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(view_instance, request, *args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return Response(
                    {"error": "Token no proporcionado"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            try:
                # Extraer el token
                prefix, token = auth_header.split(' ')
                if prefix not in ['JWT', 'Bearer']:
                    return Response(
                        {"error": "Formato de token inválido"},
                        status=status.HTTP_401_UNAUTHORIZED
                    )

                # Primero verificamos el token localmente
                try:
                    payload = verify_jwt_token(token)
                    logger.info(f"Token verificado localmente: {payload}")
                except AuthenticationFailed as e:
                    return Response(
                        {"error": str(e)},
                        status=status.HTTP_401_UNAUTHORIZED
                    )

                # Si el token es válido, verificamos la identidad con el servicio de autenticación
                response = requests.get(
                    f"{os.getenv('AUTH_SERVICE_HOST')}/auth/users/me/",
                    headers={"Authorization": f"JWT {token}"}
                )
                response.raise_for_status()
                
                user_details = response.json()
                logger.info(f"User details: {user_details}")
                
                # Almacenar el ID de usuario y detalles para uso en la vista
                request.user_id = user_details.get('id')
                request.user_details = user_details

                # Si todo está bien, continuar con la vista
                return view_func(view_instance, request, *args, **kwargs)

            except requests.exceptions.RequestException as e:
                logger.error(f"Error al contactar el servicio de autenticación: {str(e)}")
                return Response(
                    {"error": "Error al contactar el servicio de autenticación"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            except Exception as e:
                logger.error(f"Error inesperado: {str(e)}")
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return _wrapped_view
    return decorator