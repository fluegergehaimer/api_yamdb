from django.urls import include, path
from rest_framework import routers

from .views import (AuthenticationAPIView, RegistrationAPIView,
                    UserRetrieveUpdateViewSet, UserViewSet)

app_name = 'users'

router_v1 = routers.DefaultRouter()
router_v1.register(r"", UserViewSet, basename="users",)

urlpatterns = [
    path("signup/", RegistrationAPIView.as_view(), name="signup"),
    path("token/", AuthenticationAPIView.as_view(), name="token"),
    path("me/", UserRetrieveUpdateViewSet.as_view(
        {'get': 'retrieve', 'patch': 'update'}
    ), name="me"),
    path("", include(router_v1.urls)),
]

