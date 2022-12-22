from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import ProtectedError

from django.contrib.messages.views import SuccessMessageMixin

from django.utils.translation import gettext_lazy as _

from task_manager.mixins import CustomLoginRequiredMixin
from task_manager.labels import models, forms


_CREATE_LABEL_SUCCESS_MESSAGE = _('Label successfully created')
_UPDATE_LABEL_SUCCESS_MESSAGE = _('Label successfully updated')
_DELETE_LABEL_SUCCESS_MESSAGE = _('Label successfully deleted')
_DELETE_LABEL_ERROR_MESSAGE = _('It is impossible to delete a'
                                ' label because it is in use')


class LabelListView(CustomLoginRequiredMixin,
                    generic.ListView):
    model = models.TaskLabel
    template_name = 'labels/list.html'


class LabelCreateView(CustomLoginRequiredMixin,
                      SuccessMessageMixin,
                      generic.CreateView):
    form_class = forms.TaskLabelForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels:list')
    success_message = _CREATE_LABEL_SUCCESS_MESSAGE


class LabelUpdateView(CustomLoginRequiredMixin,
                      SuccessMessageMixin,
                      generic.UpdateView):
    model = models.TaskLabel
    form_class = forms.TaskLabelForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels:list')
    success_message = _UPDATE_LABEL_SUCCESS_MESSAGE


class LabelDeleteView(CustomLoginRequiredMixin,
                      generic.DeleteView):
    model = models.TaskLabel
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels:list')
    success_message = _DELETE_LABEL_SUCCESS_MESSAGE
    error_url = reverse_lazy('statuses:list')
    error_message = _DELETE_LABEL_ERROR_MESSAGE

    def form_valid(self, form):
        try:
            self.object.delete()
        except ProtectedError:
            messages.error(self.request, self.error_message)
            return redirect(self.error_url)
        messages.success(self.request, self.success_message)
        return redirect(self.success_url)
