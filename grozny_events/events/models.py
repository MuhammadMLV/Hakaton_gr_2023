from django.contrib.auth import get_user_model
from django.db import models

FIRST_SYMBOLS = 20

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=90, verbose_name='Наименование')
    slug = models.SlugField(max_length=30, unique=True, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')
    category = models.ForeignKey(
        Category, blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name='events',
        verbose_name='Категория',
        help_text='Категория, к которой будет относиться мероприятие',
    )
    pub_date = models.DateTimeField(auto_now=True, verbose_name='Дата публикации')
    date = models.DateTimeField(verbose_name='Дата проведения')
    location = models.CharField(
        max_length=250, blank=False,
        null=False, verbose_name='Место проведения'
    )
    description = models.TextField(verbose_name='Описание мероприятия')
    additionally = models.CharField(
        max_length=250, verbose_name='Дополнительно',
        blank=True, null=True,
    )
    organizer = models.ForeignKey(
        User,
        verbose_name='Организатор',
        on_delete=models.CASCADE,
        related_name='events',
        )
    image = models.ImageField(
        blank=True,
        upload_to='posts/',
        verbose_name='Изображение',
        help_text='Изображение для публикации'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'

    def __str__(self):
        return self.title[:FIRST_SYMBOLS]


class Comment(models.Model):
    RATE_CHOICES = (
        (1, 'Ужасно'),
        (2, 'Плохо'),
        (3, 'Удовлетворительно'),
        (4, 'Хорошо'),
        (5, 'Отлично'),
    )
    event = models.ForeignKey(
        Event,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Мероприятие',
    )
    author = models.ForeignKey(
        User,
        related_name='comments',
        verbose_name='Автор',
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        verbose_name='Комментарий',
        help_text='Комментария для мероприятия'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата написания'
    )
    rate = models.SmallIntegerField(
        verbose_name='Рейтинг',
        choices=RATE_CHOICES,
    )

    class Meta:
        ordering = ('-created', )
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE,
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_user_author'
            )
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
