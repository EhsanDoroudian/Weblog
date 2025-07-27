import os
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static
import sys

# Detect if running tests
TESTING = 'test' in sys.argv or 'PYTEST_VERSION' in os.environ

# drf-yasg Schema View Configuration
schema_view = get_schema_view(
    openapi.Info(
        title="Blog API Documentation",
        default_version='v1',
        description="API endpoints for Blog and Comment system",
        terms_of_service="https://www.yoursite.com/terms/",
        contact=openapi.Contact(email="contact@yoursite.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin and authentication
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    
    # Your app URLs
    path('blogs/', include('blogs.urls')),
    path('api/', include('blogs.api.api_urls')),
    path('', include('blogs.urls')),  # Default/homepage
    
    # API Documentation URLs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    path('swagger/',
         schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/',
         schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]

# Add debug toolbar URLs only in DEBUG mode and not testing
if settings.DEBUG and not TESTING:
    urlpatterns = [path('__debug__/', include('debug_toolbar.urls'))] + urlpatterns

# Serve static files in production
if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)