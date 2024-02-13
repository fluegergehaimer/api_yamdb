from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r"", UserViewSet, basename="users")

urlpatterns = [
    # path("v1/", include("djoser.urls.jwt")),
    path("", include(router_v1.urls)),
]