"""loun URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

from config.routers import DefaultRouter
from users.views import UserViewSet, UserLoginView, FriendRequestViewSet

admin.site.site_header = "Django"
admin.site.site_title = "Django"
admin.site.index_title = "Home"
admin.site.site_url = None

schema_view = get_schema_view(
    openapi.Info(
        title="Django API",
        default_version="v1",
        description="Django API",
        terms_of_service="",
        contact=openapi.Contact(email=""),
        license=openapi.License(name=""),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register("users", UserViewSet)
router.register("friend-requests", FriendRequestViewSet)
router.register("devices", FCMDeviceAuthorizedViewSet, basename="devices")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/", include("djoser.urls.jwt")),
    path("auth/token/login/", TokenObtainPairView.as_view()),
    path("auth/token/refresh/", TokenRefreshView.as_view()),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("api/", include("rest_framework.urls")),
    path("pages/", include("django.contrib.flatpages.urls")),
    path("summernote/", include("django_summernote.urls")),
    re_path(r"^s3direct/", include("s3direct.urls")),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
