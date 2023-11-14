# Create custom JWTAuth for web socket authentication

import jwt
from django.contrib.auth import get_user_model

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

User = get_user_model()

@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(uid=user_id)
    except User.DoesNotExist:
        return None
        
class JWTAuthenticationMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner
            
    async def __call__(self, scope, receive, send):
        try:
            # Get token from headers list
            JWT_TOKEN = scope['headers']
            headers = dict(scope['headers'])
            if b'authorization' in headers:
                try:
                    token_key = headers[b'authorization'].decode()
                    JWT_TOKEN = token_key
                except Exception as e:
                    print("Exception: {}".format(e))
            if JWT_TOKEN:
                decoded_token = jwt.decode(JWT_TOKEN, algorithms=['HS256'])
                user_id = decoded_token['sub']
                user = await get_user(user_id)
                scope['user'] = user
        except Exception as e:
            scope['user'] = None
            print(e)
        return await super().__call__(scope, receive, send)                  
                    