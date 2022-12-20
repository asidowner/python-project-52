from django.urls import reverse_lazy
from django.views import generic

from django.shortcuts import redirect
from django.contrib import messages

from django.contrib.auth import models as auth_models
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.utils.translation import gettext_lazy as _

from task_manager.users.forms import UserCreateForm

_CREATE_USER_SUCCESS_MESSAGE = _('User is successfully registered')
_UPDATE_USER_SUCCESS_MESSAGE = _('User is successfully changed')
_UPDATE_USER_ERROR_MESSAGE = _("You don't have permission"
                               " to change another user.")
_DELETE_USER_SUCCESS_MESSAGE = _('User is successfully deleted')
_DELETE_USER_ERROR_MESSAGE = _("You don't have permission"
                               " to delete another user.")


class UserListView(generic.ListView):
    model = auth_models.User
    template_name = 'users/list.html'


class UserCreateView(SuccessMessageMixin, generic.CreateView):
    form_class = UserCreateForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('auth:login')
    success_message = _CREATE_USER_SUCCESS_MESSAGE


class UserUpdateView(LoginRequiredMixin,
                     UserPassesTestMixin,
                     SuccessMessageMixin,
                     generic.UpdateView):
    model = auth_models.User
    form_class = UserCreateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users:list')
    success_message = _UPDATE_USER_SUCCESS_MESSAGE

    def test_func(self):
        return self.kwargs['pk'] == self.request.user.id

    def handle_no_permission(self):
        messages.error(self.request, _UPDATE_USER_ERROR_MESSAGE)
        return redirect(reverse_lazy('users:list'))


class UserDeleteView(LoginRequiredMixin,
                     UserPassesTestMixin,
                     SuccessMessageMixin,
                     generic.DeleteView):
    model = auth_models.User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:list')
    success_message = _DELETE_USER_SUCCESS_MESSAGE

    def test_func(self):
        return self._is_self_user()

    def _is_self_user(self):
        return self.kwargs['pk'] == self.request.user.id

    def handle_no_permission(self):
        messages.error(self.request, _DELETE_USER_ERROR_MESSAGE)
        return redirect(reverse_lazy('users:list'))
