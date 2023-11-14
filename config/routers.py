from django.urls import re_path, include

from rest_framework.routers import DefaultRouter as BaseDefaultRouter, Route, DynamicRoute
from rest_framework.urlpatterns import format_suffix_patterns

from rest_framework import viewsets

class DefaultRouter(BaseDefaultRouter):
    routes = [
        # List route.
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create',
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        # Dynamically generated list routes. Generated using
        # @action(detail=False) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{url_path}{trailing_slash}$', name='{basename}-{url_name}', detail=False, initkwargs={}
        ),
        # Detail route.
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        ),
        Route(
            url=r'^{prefix}/{lookup}/delete{trailing_slash}$',
            mapping={
                'delete': 'destroy'
            },
            name='{basename}-delete-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        ),
        # Dynamically generated detail routes. Generated using
        # @action(detail=True) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{lookup}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        ),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.inner_registry = []

    def get_inner_viewset(self, prefix, router):

        class InnerViewSet(viewsets.ViewSet):
            schema = None

            def list(self, request):
                view = router.get_api_root_view(api_urls=router.urls)
                return view(request._request)

            def get_view_name(self):
                return prefix.capitalize()

        return InnerViewSet

    def register_nested(self, prefix: str, router: BaseDefaultRouter):

        self.inner_registry.append((prefix, router))
        inner_viewset = self.get_inner_viewset(prefix, router)
        self.register(prefix, inner_viewset, basename=prefix)

    def get_urls(self):
        """
        Generate the list of URL patterns, including a default root view
        for the API, and appending `.json` style format suffixes.
        """
        urls = super().get_urls()

        for prefix, router in self.inner_registry:
            root_url = re_path(f'{prefix}/', include(router.urls), name=prefix)
            urls.append(root_url)

        return urls
