from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView


from . import permissions
from .models import User
from .serializers import (
    AuthenticationSerializer, RegistrationSerializer, UserSerializer
)


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     lookup_url_kwarg = 'username'
#     permission_classes = (permissions.IsAdmin,)
#     filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
#     search_fields = ('username',)
#     http_method_names = ['get', 'post', 'delete', 'patch', ]

#     def get_object(self):
#         username = self.kwargs.get('username')
#         return get_object_or_404(self.queryset, username=username)


# class UserRetrieveUpdateViewSet(
#                    mixins.RetrieveModelMixin,
#                    mixins.UpdateModelMixin,
#                    viewsets.GenericViewSet,
# ):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = (IsAuthenticated,)
#     def get_serializer_class(self):
#         print('self.action______________________________', self.action)
#         print('role____________________________', self.request.user.role)
#         if self.action == 'update':
#             return UserUpdateSerializer
#         return UserSerializer

#     def get_object(self):
#         user = self.request.user
#         return user
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdmin,)
    lookup_field = 'username'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    http_method_names = ('get', 'post', 'patch', 'delete')
    search_fields = ('username',)
    @action(
        detail=False,
        methods=('get', 'patch'),
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        if request.method == 'GET':
            user = get_object_or_404(User, id=request.user.id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        if request.method == 'PATCH':
            user = get_object_or_404(User, id=request.user.id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(role=request.user.role)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

class RegistrationAPIView(APIView):
    """
    Разрешить всем пользователям (аутентифицированным и нет) доступ к данному эндпоинту.
    """
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if not serializer.validated_data.get('is_user_exist', None):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthenticationAPIView(APIView):
    serializer_class = AuthenticationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
