import debug_toolbar
from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("ecommerce.drf.urls")),
    path("__debug__/", include(debug_toolbar.urls)),
]


schema_view = get_schema_view(
    openapi.Info(
        title="Ecommerce API",
        default_version='v1',
        description="This is an API for ecommerce application",
        # terms_of_service="https://www.google.com/policies/terms/",
        # contact=openapi.Contact(email="contact@snippets.local"),
        # license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


ui_urls = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path("", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^api/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += ui_urls