from django import forms
from django.utils.translation import gettext_lazy as _
from task_manager.statuses import models


class TaskStatusForm(forms.ModelForm):
    name = forms.CharField(
        label=_('Name'),
        widget=forms.TextInput(attrs={'placeholder': _('Name')})
    )

    class Meta:
        model = models.TaskStatus
        fields = ('name',)
