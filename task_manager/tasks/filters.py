from django import forms
from django.utils.translation import gettext_lazy as _

from django_filters import (FilterSet,
                            ModelChoiceFilter,
                            BooleanFilter)

from django.contrib.auth import models as auth_models

from task_manager.tasks import models as tasks_models
from task_manager.statuses import models as statuses_models
from task_manager.labels import models as labels_models


class TaskFilter(FilterSet):
    status = ModelChoiceFilter(
        label=_('Status'),
        queryset=statuses_models.TaskStatus.objects.all()
    )
    executor = ModelChoiceFilter(
        label=_('Executor'),
        queryset=auth_models.User.objects.all()
    )
    label = ModelChoiceFilter(
        label=_('Label'),
        field_name='labels',
        queryset=labels_models.TaskLabel.objects.all()
    )
    self_tasks = BooleanFilter(
        label='Only self tasks',
        field_name='author',
        method='filter_self_tasks',
        widget=forms.CheckboxInput
    )

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(**{name: self.request.user})
        return queryset.filter()

    class Meta:
        model = tasks_models.Task
        exclude = ['name',
                   'description',
                   'author',
                   'date_create',
                   'labels']
