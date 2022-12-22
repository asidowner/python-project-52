from django import forms
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import models as auth_models

from task_manager.tasks import models as tasks_models
from task_manager.statuses import models as statuses_models
from task_manager.labels import models as labels_models


class TaskForm(forms.ModelForm):
    name = forms.CharField(
        label=_('Name'),
        widget=forms.TextInput(attrs={'placeholder': _('Name')}),
        required=True,
    )
    description = forms.CharField(
        label=_('Description'),
        widget=forms.Textarea(attrs={'placeholder': _('Description')}),
        required=True,
    )
    status = forms.ModelChoiceField(
        queryset=statuses_models.TaskStatus.objects.all(),
        label=_('Status'),
        empty_label='---------',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    executor = forms.ModelChoiceField(
        queryset=auth_models.User.objects.all(),
        label=_('Executor'),
        empty_label='---------',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    labels = forms.ModelMultipleChoiceField(
        queryset=labels_models.TaskLabel.objects.all(),
        label=_('Labels'),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    class Meta:
        model = tasks_models.Task
        fields = ('name', 'description', 'status', 'executor', 'labels')
