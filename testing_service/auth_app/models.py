from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Таблица пользователя"""

    class Meta:
        db_table = "users"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
