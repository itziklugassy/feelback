from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from projects.views import ProjectViewSet, ProjectCategoryViewSet, RatingViewSet
from users.views import login_view, logout_view, auth_options  # Added auth_options
from django.conf import settings
from django.conf.urls.static import static

# Initialize the router for viewsets
router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'categories', ProjectCategoryViewSet)
router.register(r'ratings', RatingViewSet)

# API URLs
api_urlpatterns = [
    path('', include(router.urls)),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('auth/', auth_options, name='auth-options'),  # Added auth options endpoint
]

# Main URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urlpatterns)),  # All API routes under /api/
    path('api-auth/', include('rest_framework.urls')),  # DRF browsable API auth
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Debug toolbar URLs (optional, for development only)
if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ] if 'debug_toolbar' in settings.INSTALLED_APPS else []

# Add proper URL patterns documentation
__all__ = ['urlpatterns']

# Document available API endpoints
API_ENDPOINTS = {
    'login': '/api/login/',
    'logout': '/api/logout/',
    'auth_options': '/api/auth/',
    'projects': '/api/projects/',
    'categories': '/api/categories/',
    'ratings': '/api/ratings/',
}