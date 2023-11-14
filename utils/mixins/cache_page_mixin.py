""" this mixin set the cache-control header
    for list view and retrive view in ModelViewSet
"""

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.conf import settings


class CachePageMixin:

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(settings.CACHE_CONTROL_MAX_AGE))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)