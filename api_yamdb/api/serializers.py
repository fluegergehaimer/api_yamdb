"""Сериалайзеры."""
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Genre, GenreTitle, Title, Review, Comment


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        """Class Meta."""

        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        """Class Meta."""

        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        """Class Meta."""

        model = Title
        fields = '__all__'


class TitleCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор создания и обновления произведений."""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        required=True
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        required=True
    )
    description = serializers.CharField(required=False)

    class Meta:
        """Class Meta."""

        model = Title
        fields = '__all__'
        read_only_fields = ('rating',)

    def create(self, validated_data):
        """Create function."""
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)

        for genre in genres:
            genre = get_object_or_404(Genre, slug=genre.slug)
            GenreTitle.objects.create(genre=genre, title=title)
        return title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    score = serializers.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    class Meta:
        """Class Meta."""

        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        """Функция проверки данных."""
        if self.context['request'].method != 'POST':
            return data
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=author, title__id=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже оставили отзыв на данное произведение'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        """Class Meta."""

        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
