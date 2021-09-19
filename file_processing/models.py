from django.db import models


class File(models.Model):
    path_to_file = models.TextField(default='', verbose_name='Путь к файлу')
    words = models.TextField(default='', verbose_name='Уникальные слова')
