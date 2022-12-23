from django.views import generic
from django.urls import reverse_lazy

from django.contrib.messages.views import SuccessMessageMixin

from django_filters.views import FilterView
from django.utils.translation import gettext_lazy as _

from task_manager.mixins import CustomLoginRequiredMixin
from task_manager.tasks import models, forms, filters

_CREATE_TASK_SUCCESS_MESSAGE = _('Task successfully created')
_UPDATE_TASK_SUCCESS_MESSAGE = _('Task successfully updated')
_DELETE_TASK_SUCCESS_MESSAGE = _('Task successfully deleted')


class TaskListView(CustomLoginRequiredMixin,
                   FilterView):
    model = models.Task
    template_name = 'tasks/list.html'
    filterset_class = filters.TaskFilter


class TaskCardView(CustomLoginRequiredMixin,
                   generic.DetailView):
    model = models.Task
    template_name = 'tasks/card.html'


class TaskCreateView(CustomLoginRequiredMixin,
                     SuccessMessageMixin,
                     generic.CreateView):
    form_class = forms.TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks:list')
    success_message = _CREATE_TASK_SUCCESS_MESSAGE

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(TaskCreateView, self).form_valid(form)


class TaskUpdateView(CustomLoginRequiredMixin,
                     SuccessMessageMixin,
                     generic.UpdateView):
    model = models.Task
    form_class = forms.TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks:list')
    success_message = _UPDATE_TASK_SUCCESS_MESSAGE


class TaskDeleteView(CustomLoginRequiredMixin,
                     SuccessMessageMixin,
                     generic.DeleteView):
    model = models.Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks:list')
    success_message = _DELETE_TASK_SUCCESS_MESSAGE
