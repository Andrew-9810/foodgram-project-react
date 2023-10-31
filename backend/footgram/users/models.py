from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='filed_verbose_name_Электронная почта'
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='filed_verbose_name_Имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='filed_verbose_name_Фамилия'
    )
    # REQUIRED_FIELDS должен содержать все обязательные поля в вашей пользовательской модели,
    # но не должен содержать USERNAME_FIELD или, так password
    # как эти поля всегда будут запрашиваться.
    USERNAME_FIELD = 'email'
    # Список имен полей, которые будут запрошены при создании пользователя
    # с помощью команды createsuperuserуправления.
    # Пользователю будет предложено ввести значение для каждого из этих полей.
    # Она должна включать в себя любое поле , для которого blank является False
    # или неопределенным и может включать в себя дополнительные поля ,
    # которые вы хотите запрашиваться при создании пользователя в интерактивном режиме .
    # REQUIRED_FIELDS не влияет на другие части Django,
    # например на создание пользователя в админке.
    # REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = "verbose_name_Пользователь"
        verbose_name_plural = "verbose_name_plural_Пользователи"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Follow(models.Model):
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
            )
        ]

    def __str__(self):
        return f'Подписчик: {self.user}, автор: {self.author}'
