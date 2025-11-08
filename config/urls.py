from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="ONETOUCH API",
        default_version='v1',
        description="Документация API для проекта ONETOUCH",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
<<<<<<< HEAD
    path('api/admin/', admin.site.urls),
    path('api/auth/', include('social_django.urls', namespace='social')),
=======
    # Админка
    path('api/admin/', admin.site.urls),

    # Социальная авторизация
    path('auth/', include('social_django.urls', namespace='social')),
>>>>>>> f1e4b04 (apps)

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

<<<<<<< HEAD
    path('api/', include('user.urls')),
    path('api/', include('api.urls')),
    path('api/', include('reservation.urls')),

    path('api/ONETOUCH/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
=======
    # APPS
    path('api/user/', include('apps.user.urls')),
    path('api/', include('apps.main.urls')),
    path("api/payment", include('apps.payment.urls')),

    # Swagger / Redoc
    path('api/car-wash.api/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
>>>>>>> f1e4b04 (apps)
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
]

# Статика и медиа 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

