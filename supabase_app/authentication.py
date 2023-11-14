from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
import json
from django.conf import settings
from .supabase_app import supabase

User = get_user_model()

class SupabaseAuthentication(authentication.BaseAuthentication):
    """
    Supabase Authentication based Django rest framework authentication class.

    Clients should authenticate by passing a Supabase JWT in the
    "Authorization" HTTP header, prepended with the string "<keyword> " where
    <keyword> is this classes `keyword` string property. For example:

    Authorization:Token xxxxx.yyyyy.zzzzz
    """

    keyword = 'Token'

    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise AuthenticationFailed(msg)
        if len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise AuthenticationFailed(msg)

        try:
            jwt_token = auth[1].decode()
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise AuthenticationFailed(msg)

        return self.authenticate_credentials(jwt_token)

    def authenticate_credentials(self, jwt_token):
        try:
            decoded_token = jwt.decode(jwt_token, settings.SUPABASE_CONFIG['SUPABASE_JWT_SECRET'], algorithms=['HS256'], audience="authenticated")
        except jwt.ExpiredSignatureError:
            msg = 'The Supabase token has expired.'
            raise AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            msg = 'The Supabase token is invalid.'
            raise AuthenticationFailed(msg)
        
        user_id = decoded_token.get('sub')

        if not user_id:
            msg = 'No user ID found in the token.'
            raise AuthenticationFailed(msg)

        # Fetch the user or create a new user if not exist
        try:
            user = User.objects.get(uid=user_id)
        # If a new user was created, you may want to set additional fields
        except User.DoesNotExist:
            # Fetch the user's details from the database
            result = json.loads(supabase.auth.get_user(jwt_token).json())
            user = User.objects.create_user(
                uid=result["user"]["id"],
                email=result['user']['email'],
                phone_number=result['user']['phone'],
            )

        return (user, decoded_token)


    def authenticate_header(self, request):
        """
        Returns a string that will be used as the value of the WWW-Authenticate
        header in a HTTP 401 Unauthorized response.
        """
        return self.keyword
