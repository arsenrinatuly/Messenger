from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, RegistrationViewSet


router = DefaultRouter()
router.register(
    prefix="registration", viewset=RegistrationViewSet,
    basename="registration"
)

router.register(
    prefix="users", viewset=UserViewSet, 
    basename="users"
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/v1/", include(router.urls)),
]
