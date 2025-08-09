from django.core.management.base import BaseCommand
from users.models import AppUser
from videos.models import Video
import random

class Command(BaseCommand):
    help = 'Fast generate 10k users and 100k published videos'

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