from django.contrib import admin
from task_manager.labels.models import TaskLabel


class TaskLabelAdmin(admin.ModelAdmin):
    pass


admin.site.register(TaskLabel, TaskLabelAdmin)
