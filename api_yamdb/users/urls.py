from django.urls import include, path
from rest_framework import routers

from .views import UserProfileViewSet, UserViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r"me/", UserProfileViewSet, basename="me",)
router_v1.register(r"", UserViewSet, basename="users",)

urlpatterns = [
    path("", include(router_v1.urls)),
]
