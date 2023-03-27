from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class News(models.Model):
    title = models.CharField('Заголовок', max_length=255)
    text = models.TextField('Текст', max_length=49_000)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='news', verbose_name='Автор'
    )
<<<<<<< HEAD
    likes = models.IntegerField('Количество лайков')
    published = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique author news')
        ]
=======
    likes = models.IntegerField('Количество лайков', default=0)
    published = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
>>>>>>> dev
        ordering = ['-published']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return f'News {self.pk} {self.title}:{self.text[:15]}'


class Comment(models.Model):
    text = models.TextField('Текст', max_length=4096)
    author = models.ForeignKey(
<<<<<<< HEAD
        User, on_delete=models.CASCADE, related_name='comments',
=======
        User, on_delete=models.DO_NOTHING, related_name='comments',
>>>>>>> dev
        verbose_name='Автор'
    )
    news = models.ForeignKey(
        News, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Новость'
    )
    published = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ['-published']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Comment {self.pk} {self.author}:{self.text[:15]}'
<<<<<<< HEAD
=======


class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name='liked_news',
        verbose_name='Лайки', db_index=True,
    )
    news = models.ForeignKey(
        News, on_delete=models.CASCADE, related_name='liked_users',
        verbose_name='Лайки', db_index=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'news'],
                name='unique likes')
        ]
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
>>>>>>> dev
