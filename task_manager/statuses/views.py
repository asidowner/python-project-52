from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import ProtectedError

from django.contrib.messages.views import SuccessMessageMixin

from django.utils.translation import gettext_lazy as _

from task_manager.mixins import CustomLoginRequiredMixin
from task_manager.statuses import models, forms

_CREATE_STATUS_SUCCESS_MESSAGE = _('Status successfully created')
_UPDATE_STATUS_SUCCESS_MESSAGE = _('Status successfully updated')
_DELETE_STATUS_SUCCESS_MESSAGE = _('Status successfully deleted')
_DELETE_STATUS_ERROR_MESSAGE = _('It is impossible to delete a'
                                 ' status because it is in use')


class StatusListView(CustomLoginRequiredMixin,
                     generic.ListView):
    model = models.TaskStatus
    template_name = 'statuses/list.html'


class StatusCreateView(CustomLoginRequiredMixin,
                       SuccessMessageMixin,
                       generic.CreateView):
    form_class = forms.TaskStatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses:list')
    success_message = _CREATE_STATUS_SUCCESS_MESSAGE


class StatusUpdateView(CustomLoginRequiredMixin,
                       SuccessMessageMixin,
                       generic.UpdateView):
    model = models.TaskStatus
    form_class = forms.TaskStatusForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses:list')
    success_message = _UPDATE_STATUS_SUCCESS_MESSAGE


class StatusDeleteView(CustomLoginRequiredMixin,
                       SuccessMessageMixin,
                       generic.DeleteView):
    model = models.TaskStatus
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses:list')
    success_message = _DELETE_STATUS_SUCCESS_MESSAGE
    error_url = reverse_lazy('statuses:list')
    error_message = _DELETE_STATUS_ERROR_MESSAGE

    def form_valid(self, form):
        try:
            self.object.delete()
        except ProtectedError:
            messages.error(self.request, self.error_message)
            return redirect(self.error_url)
        return redirect(self.success_url)
