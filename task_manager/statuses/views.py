from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.utils.translation import gettext_lazy as _

from task_manager.statuses import models
from task_manager.statuses import forms

from task_manager.tasks.models import Task

_CREATE_STATUS_SUCCESS_MESSAGE = _('Status successfully created')
_UPDATE_STATUS_SUCCESS_MESSAGE = _('Status successfully updated')
_DELETE_STATUS_SUCCESS_MESSAGE = _('Status successfully deleted')
_DELETE_STATUS_ERROR_MESSAGE = _('It is impossible to delete a'
                                 ' status because it is in use')


class StatusListView(LoginRequiredMixin,
                     generic.ListView):
    model = models.TaskStatus
    template_name = 'statuses/list.html'


class StatusCreateView(LoginRequiredMixin,
                       SuccessMessageMixin,
                       generic.CreateView):
    form_class = forms.TaskStatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses:list')
    success_message = _CREATE_STATUS_SUCCESS_MESSAGE


class StatusUpdateView(LoginRequiredMixin,
                       SuccessMessageMixin,
                       generic.UpdateView):
    model = models.TaskStatus
    form_class = forms.TaskStatusForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses:list')
    success_message = _UPDATE_STATUS_SUCCESS_MESSAGE


class StatusDeleteView(LoginRequiredMixin,
                       SuccessMessageMixin,
                       UserPassesTestMixin,
                       generic.DeleteView):
    model = models.TaskStatus
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses:list')
    success_message = _DELETE_STATUS_SUCCESS_MESSAGE

    def test_func(self):
        return self._is_have_task_with_this_status()

    def _is_have_task_with_this_status(self):
        return not Task.objects.filter(status_id=self.kwargs['pk']).exists()

    def handle_no_permission(self):
        messages.error(self.request, _DELETE_STATUS_ERROR_MESSAGE)
        return redirect(reverse_lazy('statuses:list'))
