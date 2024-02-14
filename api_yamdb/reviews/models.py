from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

from users.models import User


MESSAGE_1 = 'Оценка не может быть ниже 1.'
MESSAGE_2 = 'Оценка не может быть выше 10.'
TEXT_LIMIT = 20

class NameSlugModel(models.Model):
    name = models.CharField(
        verbose_name='title',
        max_length=128,
    )
    slug = models.SlugField(
        verbose_name='slug',
        unique=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[:TEXT_LIMIT]


class Genre(NameSlugModel):
    class Meta:
        verbose_name = 'genre'
        verbose_name_plural = 'genres'
        ordering = ('name',)

        def __str__(self) -> str:
            return self.name[:TEXT_LIMIT]


class Category(NameSlugModel):
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ('name',)

        def __str__(self) -> str:
            return self.name[:TEXT_LIMIT]


class Title(models.Model):
    name = models.CharField(
        verbose_name='title',
        max_length=128,
    )
    year = models.SmallIntegerField(
        verbose_name='year',
        validators=[
            MinValueValidator(1888),
            MaxValueValidator(timezone.now().year),
        ]
    )
    description = models.TextField(
        verbose_name='description',
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='genre',
        related_name='title_genre'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='category',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='title_category'
    )

    class Meta:
        verbose_name = 'work'
        verbose_name_plural = 'works'
        ordering = ('year', 'name')

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )

    class Meta:
        verbose_name = 'Жанры произведения'
        verbose_name_plural = 'Жанры произведений'

    def __str__(self):
        return f'{self.title} принадлежит жанру {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField(
        verbose_name='Text of feedback',
        help_text='Оставить отзыв.',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, MESSAGE_1),
            MaxValueValidator(10, MESSAGE_2)
        ],
        verbose_name='Grade',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        verbose_name = 'review'
        verbose_name_plural = 'reviews'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique_review'
            )
        ]

    def __str__(self):
        return f'{self.text[:TEXT_LIMIT]}, {self.score}'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField(
        verbose_name='comment_text',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'comments'
        verbose_name_plural = 'comments'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:TEXT_LIMIT]
