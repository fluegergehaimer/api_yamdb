"""Views."""
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.filters import TitleFilter
from api.serializers import (
    CategorySerializer, CommentSerializer,
    GenreSerializer, ReviewSerializer,
    TitleCreateUpdateSerializer, TitleSerializer,
)
from reviews.models import Category, Genre, Review, Title
from users import permissions


HTTP_METHODS = ('get', 'post', 'patch', 'delete')


class CategoryGenreMixin(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """Базовый класс."""

    permission_classes = (permissions.IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    ordering = ('id',)


class CategoriesViewSet(CategoryGenreMixin):
    """Класс категории."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenresViewSet(CategoryGenreMixin):
    """Класс жанры."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    """Класс произведения."""

    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    ).order_by('year', 'name')
    serializer_class = TitleSerializer
    permission_classes = (permissions.IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    http_method_names = HTTP_METHODS
    filterset_class = TitleFilter

    def get_serializer_class(self):
        """Функция определения сериализатора."""
        if self.request.method == 'GET':
            return TitleSerializer
        return TitleCreateUpdateSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Класс отзывы."""

    serializer_class = ReviewSerializer
    permission_classes = (
        permissions.IsAuthorModeratorAdminOrReadOnly,
        IsAuthenticatedOrReadOnly
    )
    filter_backends = (filters.OrderingFilter,)
    http_method_names = HTTP_METHODS

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        """Функция get_queryset."""
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        """Функция perfom_create."""
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Класс комментарии."""

    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthorModeratorAdminOrReadOnly,
        IsAuthenticatedOrReadOnly
    )
    filter_backends = (filters.OrderingFilter,)
    http_method_names = HTTP_METHODS

    def get_review(self):
        return get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id')
        )

    def perform_create(self, serializer):
        """Функция perfom_create."""
        serializer.save(author=self.request.user, review=self.get_review())

    def get_queryset(self):
        """Функция get_queryset."""
        return self.get_review().comments.all()
