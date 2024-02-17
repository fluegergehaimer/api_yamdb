import csv

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User


TABLES = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
    GenreTitle: 'genre_title.csv',

}


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for model, file in TABLES.items():
            with open(
                f'{settings.BASE_DIR}/static/data/{file}',
                'r',
                encoding='utf-8'
            ) as csv_file:
                reader = csv.DictReader(csv_file)
                model.objects.bulk_create(
                    model(**data) for data in reader)
       # self.stdout.write(self.style.SUCCESS('Данные загружены.'))
