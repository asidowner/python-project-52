from django.db import models


class TaskStatus(models.Model):
    name = models.CharField(max_length=100, unique=True)
    date_create = models.DateTimeField(auto_now_add=True)
