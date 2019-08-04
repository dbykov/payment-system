from django.db import models


class DateMixin(models.Model):
    """
    Добавляет в класс поля с датой создания и изменения записи
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время создания записи')
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата и время изменения записи')

    class Meta:
        abstract = True
