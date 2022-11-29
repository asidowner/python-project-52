from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.auth import views as auth_views
from django.utils.translation import gettext_lazy


class LoginView(SuccessMessageMixin, auth_views.LoginView):
    success_message = gettext_lazy("You're successfully logged in")
    template_name = 'auth/login.html'

    def get_success_message(self, cleaned_data):
        return self.success_message


class LogoutView(SuccessMessageMixin, auth_views.LogoutView):
    success_message = gettext_lazy("You're successfully exited")

    def get_success_message(self, cleaned_data):
        return self.success_message
