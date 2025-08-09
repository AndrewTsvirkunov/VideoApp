from django.db import models
from django.conf import settings

class Video(models.Model):
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




