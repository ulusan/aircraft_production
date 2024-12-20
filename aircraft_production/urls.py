from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
import debug_toolbar
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from parts.views import RegisterView
from django.urls import path
from parts.views import AircraftAssemblyView

schema_view = get_schema_view(
    openapi.Info(
        title="Aircraft Production API",
        default_version='v1',
        description="API documentation for Aircraft Production",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

def home_view(request):
    return HttpResponse("<h1>Welcome to the Aircraft Production Application</h1>")

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('parts.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('assemble-aircraft/', AircraftAssemblyView.as_view(), name='assemble_aircraft'),

]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
