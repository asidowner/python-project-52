from django.contrib import admin
from task_manager.statuses.models import TaskStatus


class TaskStatusAdmin(admin.ModelAdmin):
    pass


admin.site.register(TaskStatus, TaskStatusAdmin)
