from django.db import models
from django.conf import settings

class Video(models.Model):
    """
    Модель видео.

    Атрибуты:
        owner (AppUser): Пользователь, загрузивший видео.
        name (str): Название видео.
        is_published (bool): Флаг публикации видео.
        total_likes (int): Общее количество лайков.
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='videos', on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    total_likes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.name}'


class VideoFile(models.Model):
    """
    Модель файла видео, привязанного к сущности Video.

    Один объект VideoFile соответствует одному загруженному файлу (например file.mp4)
    с указанием качества. У одной записи Video может быть несколько VideoFile
    с разными значениями поля `quality` (HD, FHD, UHD).

    Атрибуты:
        video (ForeignKey): ссылка на родительское Video (related_name='files').
        file (FileField): файл медиа (upload_to='videos/').
        quality (str): качество видео — 'HD', 'FHD' или 'UHD'.
    """
    QUALITY_HD = 'HD'
    QUALITY_FHD = 'FHD'
    QUALITY_UHD = 'UHD'
    QUALITY_CHOICES = [
        (QUALITY_HD, 'HD (720p)'),
        (QUALITY_FHD, 'FHD (1080p)'),
        (QUALITY_UHD, 'UHD (4k)')
    ]

    video = models.ForeignKey(Video, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='videos/')
    quality = models.CharField(max_length=3, choices=QUALITY_CHOICES)

    def __str__(self):
        return f'{self.video_id} / {self.quality}'


class Like(models.Model):
    """
    Модель лайка — связь "пользователь - видео".

    Каждый лайк хранит, какой пользователь поставил лайк какому видео и время создания.
    Введено уникальное ограничение (video, user), чтобы пользователь не мог поставить
    больше одного лайка на одно видео.

    Атрибуты:
        video (ForeignKey): видео, которому поставлен лайк (related_name='likes').
        user (ForeignKey): пользователь, поставивший лайк (related_name='likes').
        created_at (DateTime): время установки лайка (auto_now_add=True).

    Meta:
        - unique constraint 'unique_like_user_video' на полях (video, user)
        - индекс по (video, user) для ускорения поиска/удаления
    """
    video = models.ForeignKey(Video, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['video', 'user'], name='unique_like_user_video')
        ]
        indexes = [
            models.Index(fields=['video', 'user'])
        ]




