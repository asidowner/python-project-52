from django.views import generic
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.utils.translation import gettext_lazy as _

from task_manager.statuses import models
from task_manager.statuses import forms

_CREATE_STATUS_SUCCESS_MESSAGE = _('Status successfully created')
_UPDATE_STATUS_SUCCESS_MESSAGE = _('Status successfully updated')
_DELETE_STATUS_SUCCESS_MESSAGE = _('Status successfully deleted')


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
                       generic.DeleteView):
    model = models.TaskStatus
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses:list')
    success_message = _DELETE_STATUS_SUCCESS_MESSAGE
