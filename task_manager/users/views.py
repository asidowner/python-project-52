from django.urls import reverse_lazy
from django.views import generic

from django.shortcuts import redirect
from django.contrib import messages

from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import ProtectedError
from django.contrib.auth import models as auth_models
from django.contrib.messages.views import SuccessMessageMixin

from django.utils.translation import gettext_lazy as _

from task_manager.mixins import CustomLoginRequiredMixin
from task_manager.users.forms import UserCreateForm

_CREATE_USER_SUCCESS_MESSAGE = _('User is successfully registered')
_CREATE_USER_ERROR_MESSAGE = _("You're already sign up...")
_UPDATE_USER_SUCCESS_MESSAGE = _('User is successfully changed')
_UPDATE_USER_PERMISSION_ERROR_MESSAGE = _("You don't have permission"
                                          " to change another user.")
_DELETE_USER_SUCCESS_MESSAGE = _('User is successfully deleted')
_DELETE_USER_PERMISSION_ERROR_MESSAGE = _("You don't have permission"
                                          " to delete another user.")
_DELETE_USER_USED_ERROR_MESSAGE = _('Unable to delete a user'
                                    ' because he is being used')


class UserListView(generic.ListView):
    model = auth_models.User
    template_name = 'users/list.html'


class UserCreateView(UserPassesTestMixin,
                     SuccessMessageMixin,
                     generic.CreateView):
    form_class = UserCreateForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('auth:login')
    success_message = _CREATE_USER_SUCCESS_MESSAGE
    error_url = reverse_lazy('home')
    error_message_permission = _CREATE_USER_ERROR_MESSAGE

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(self.request, self.error_message_permission)
        return redirect(self.error_url)


class UserUpdateView(CustomLoginRequiredMixin,
                     SuccessMessageMixin,
                     generic.UpdateView):
    model = auth_models.User
    form_class = UserCreateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users:list')
    success_message = _UPDATE_USER_SUCCESS_MESSAGE
    error_url = reverse_lazy('users:list')
    error_message_permission = _UPDATE_USER_PERMISSION_ERROR_MESSAGE

    def form_valid(self, form):
        if not self._is_self_user():
            messages.error(self.request, self.error_message_permission)
            return redirect(self.error_url)
        return super(UserUpdateView, self).form_valid(form)

    def _is_self_user(self) -> bool:
        return self.kwargs['pk'] == self.request.user.id


class UserDeleteView(CustomLoginRequiredMixin,
                     SuccessMessageMixin,
                     generic.DeleteView):
    model = auth_models.User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:list')
    success_message = _DELETE_USER_SUCCESS_MESSAGE
    error_url = reverse_lazy('users:list')
    error_message_is_used = _DELETE_USER_USED_ERROR_MESSAGE
    error_message_permission = _DELETE_USER_PERMISSION_ERROR_MESSAGE

    def form_valid(self, form):
        if not self._is_self_user():
            messages.error(self.request, self.error_message_permission)
            return redirect(self.error_url)
        try:
            self.object.delete()
        except ProtectedError:
            messages.error(self.request, self.error_message_is_used)
            return redirect(self.error_url)
        return redirect(self.success_url)

    def _is_self_user(self) -> bool:
        return self.kwargs['pk'] == self.request.user.id
