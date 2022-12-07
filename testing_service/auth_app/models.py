from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Table user"""

    class Meta:
        db_table = "users"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
