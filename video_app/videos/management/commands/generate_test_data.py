from django.core.management.base import BaseCommand
from users.models import AppUser
from videos.models import Video
import random

class Command(BaseCommand):
    """
       Management-команда для генерации тестовых данных.

       Создаёт:
           - 10 000 пользователей
           - 100 000 видео (is_published=True)

       Оптимизировано для минимизации числа запросов в базу данных:
           - Пользователи создаются батчами через bulk_create
           - Видео создаются батчами по 1000 штук
       """

    help = "Генерирует тестовые данные: 10k пользователей и 100k видео."

    def handle(self, *args, **options):
        self.stdout.write('Creating users...')
        # Создаем пользователей пачкой (bulk_create)
        users = [AppUser(username=f'user{i}') for i in range(10000)]
        AppUser.objects.bulk_create(users, batch_size=1000)

        # Загружаем их обратно, чтобы были id
        users = list(AppUser.objects.all())

        self.stdout.write('Creating videos...')
        videos = []
        for i in range(100000):
            owner = random.choice(users)
            videos.append(Video(owner=owner, is_published=True, name=f'video_{i}', total_likes=random.randint(0, 20)))
            if len(videos) >= 5000:
                Video.objects.bulk_create(videos, batch_size=5000)
                videos.clear()

        if videos:
            Video.objects.bulk_create(videos, batch_size=5000)

        self.stdout.write(self.style.SUCCESS('Done'))