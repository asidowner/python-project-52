from django.views import generic
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.utils.translation import gettext_lazy as _

from task_manager.tasks import models
from task_manager.tasks import forms

_CREATE_TASK_SUCCESS_MESSAGE = _('Task successfully created')
_UPDATE_TASK_SUCCESS_MESSAGE = _('Task successfully updated')
_DELETE_TASK_SUCCESS_MESSAGE = _('Task successfully deleted')


class TaskListView(LoginRequiredMixin,
                   generic.ListView):
    model = models.Task
    template_name = 'tasks/list.html'


class TaskCreateView(LoginRequiredMixin,
                     SuccessMessageMixin,
                     generic.CreateView):
    form_class = forms.TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks:list')
    success_message = _CREATE_TASK_SUCCESS_MESSAGE

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(TaskCreateView, self).form_valid(form)


class TaskUpdateView(LoginRequiredMixin,
                     SuccessMessageMixin,
                     generic.UpdateView):
    model = models.Task
    form_class = forms.TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks:list')
    success_message = _UPDATE_TASK_SUCCESS_MESSAGE


class TaskDeleteView(LoginRequiredMixin,
                     SuccessMessageMixin,
                     generic.DeleteView):
    model = models.Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks:list')
    success_message = _DELETE_TASK_SUCCESS_MESSAGE
