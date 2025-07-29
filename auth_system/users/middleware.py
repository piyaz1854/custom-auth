import jwt
import os
from django.utils.deprecation import MiddlewareMixin
from users.models import CustomUser
from django.conf import settings
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')


class JWTAuthenticationMiddleware(MiddlewareMixin):
    
    def process_request(self, request):
        if getattr(request, 'user', None) and request.user.is_authenticated:
            return
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = payload.get('user_id')
                user = CustomUser.objects.get(id=user_id, is_active=True)
                request.user = user
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, KeyError):
                pass
