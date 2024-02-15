from django.urls import include, path
from rest_framework import routers

from .views import AuthenticationAPIView, RegistrationAPIView, UserRetrieveUpdateViewSet, UserViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r"users", UserViewSet, basename="users",)
print(router_v1.urls)

urlpatterns = [
    path("auth/signup/", RegistrationAPIView.as_view(), name="signup"),
    path("auth/token/", AuthenticationAPIView.as_view(), name="token"),
    path("users/me/", UserRetrieveUpdateViewSet.as_view({'get': 'retrieve', 'patch': 'update'}), name="me"),
    path("", include(router_v1.urls)),
]

