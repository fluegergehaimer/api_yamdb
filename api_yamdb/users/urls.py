from django.urls import include, path
from rest_framework import routers

from .views import (AuthenticationAPIView, RegistrationAPIView,
                    UserRetrieveUpdateViewSet, UserViewSet)

app_name = 'users'

router_v1 = routers.DefaultRouter()
router_v1.register(r"", UserViewSet, basename="users",)

urlpatterns = [
    path("v1/auth/signup/", RegistrationAPIView.as_view(), name="signup"),
    path("v1/auth/token/", AuthenticationAPIView.as_view(), name="token"),
    path("v1/users/me/", UserRetrieveUpdateViewSet.as_view(
        {'get': 'retrieve', 'patch': 'update'}
    ), name="me"),
    path("v1/users/", include(router_v1.urls)),
    path("", include("api.urls")),
]

