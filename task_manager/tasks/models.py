from django.db import models


class Task(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    status = models.ForeignKey('statuses.TaskStatus',
                               on_delete=models.PROTECT,
                               related_name='statuses')
    executor = models.ForeignKey('auth.User',
                                 on_delete=models.PROTECT,
                                 related_name='executors')
    author = models.ForeignKey('auth.User',
                               on_delete=models.PROTECT,
                               related_name='authors')
    date_create = models.DateTimeField(auto_now_add=True)
