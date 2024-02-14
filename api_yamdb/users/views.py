from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = 'username'

    def get_object(self):
        username = self.kwargs.get('username')
        return get_object_or_404(self.queryset, username=username)


class UserProfileViewSet(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
