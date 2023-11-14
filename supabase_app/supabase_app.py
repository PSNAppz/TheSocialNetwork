from django.core.exceptions import ImproperlyConfigured
from supabase import create_client, Client

from .settings import SUPABASE_CONFIG

SUPABASE_JWT_SECRET = SUPABASE_CONFIG['SUPABASE_JWT_SECRET']
SUPABASE_URL = SUPABASE_CONFIG['SUPABASE_URL']
SUPABASE_SERVICE_ROLE_KEY = SUPABASE_CONFIG['SUPABASE_SERVICE_ROLE_KEY']

if not SUPABASE_JWT_SECRET:
    raise ImproperlyConfigured('you must set SUPABASE_JWT_SECRET')

if not SUPABASE_URL:
    raise ImproperlyConfigured('you must set SUPABASE_URL')

if not SUPABASE_SERVICE_ROLE_KEY:
    raise ImproperlyConfigured('you must set SUPABASE_SERVICE_ROLE_KEY')

# Initialize the Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


