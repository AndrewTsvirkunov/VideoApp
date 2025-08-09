from django.contrib.auth.models import AbstractUser

class AppUser(AbstractUser):
    """
    Кастомная модель пользователя приложения VideoApp.
    Наследуется от AbstractUser, что позволяет использовать встроенные
    механизмы аутентификации Django и при необходимости расширять поля.
    """
    def __str__(self):
        return self.username