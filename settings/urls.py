from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
<<<<<<< HEAD

from users.views import UserViewSet, RegistrationViewSet


router = DefaultRouter()
router.register(
    prefix="registration", viewset=RegistrationViewSet,
    basename="registration"
)
=======
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from users.views import UserViewSet


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
>>>>>>> d211408 (hz)

router.register(
    prefix="users", viewset=UserViewSet, 
    basename="users"
)

<<<<<<< HEAD
=======
schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version="v1",
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
>>>>>>> d211408 (hz)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/v1/", include(router.urls)),
<<<<<<< HEAD
=======
    path("swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
>>>>>>> d211408 (hz)
]
