import csv

from django.conf import settings
from django.core.management import BaseCommand
from reviews.models import (
    Category, Comment, Genre,
    GenreTitle, Review, Title, User
)

TABLES = {
    Category: 'category.csv',
    Comment: 'comments.csv',
    GenreTitle: 'genre_title.csv',
    Genre: 'genre.csv',
    Review: 'review.csv',
    Title: 'titles.csv',
    User: 'users.csv',
}


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for model, file_name in TABLES.items():
            with open(
                f'{settings.BASE_DIR}/static/data/{file_name}',
                'r',
                encoding='utf-8'
            ) as csv_data:
                reader = csv.DictReader(csv_data)
                model.objects.bulk_create(
                    model(**data) for data in reader)
