"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from api.users.views import UserRegister

schema_view = get_schema_view(
    openapi.Info(
        title="Jungle API",
        default_version='v1',
        description="Here magic happens",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="mindru.ion97@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),  # noqa
        name='schema-json'),
    url(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # noqa
    url(r'^redoc$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # noqa
    path('admin/', admin.site.urls),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include('api.nomenclatures.urls')),
    path('', include('api.users.urls')),
    path('', include('api.games.urls')),
]
