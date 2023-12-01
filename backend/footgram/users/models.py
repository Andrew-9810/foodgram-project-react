from django.contrib.auth.models import AbstractUser
from django.db import models

USER_NAME_LENGTH = 150
EMAIL_LENGTH = 254


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""
    email = models.EmailField(
        max_length=EMAIL_LENGTH,
        unique=True,
        verbose_name='Электронная почта'
    )
    first_name = models.CharField(
        max_length=USER_NAME_LENGTH,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=USER_NAME_LENGTH,
        verbose_name='Фамилия'
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Follow(models.Model):
    """Модель Подписчиков."""
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = ['user']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow_model'
            ),
            models.CheckConstraint(
                name='subscribe_to_yourself',
                check=~models.Q(user=models.F("author"))
            )
        ]

    def __str__(self):
        return f'Подписчик: {self.user}, автор: {self.author}'
