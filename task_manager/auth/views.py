from django.contrib import messages

from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.auth import views as auth_views
from django.utils.translation import gettext_lazy as _

_LOGIN_SUCCESS_MESSAGE = _("You're successfully logged in")
_LOGOUT_SUCCESS_MESSAGE = _("You're successfully exited")


class LoginView(SuccessMessageMixin, auth_views.LoginView):
    success_message = _LOGIN_SUCCESS_MESSAGE
    template_name = 'auth/login.html'

    def get_success_message(self, cleaned_data):
        return self.success_message


class LogoutView(auth_views.LogoutView):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.add_message(request, messages.INFO, _LOGOUT_SUCCESS_MESSAGE)
        return response
