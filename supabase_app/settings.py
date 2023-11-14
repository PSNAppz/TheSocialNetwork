from django.conf import settings

SUPABASE_CONFIG = getattr(settings, "SUPABASE_CONFIG", {})

# Supabase config
SUPABASE_CONFIG.setdefault("SUPABASE_JWT_SECRET", None)
SUPABASE_CONFIG.setdefault("SUPABASE_URL", None)
SUPABASE_CONFIG.setdefault("SUPABASE_SERVICE_ROLE_KEY", None)

# User model
SUPABASE_CONFIG.setdefault("USER_MODEL", settings.AUTH_USER_MODEL)
