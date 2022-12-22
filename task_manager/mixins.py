from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


class CustomLoginRequiredMixin(LoginRequiredMixin):
    """Verify that the current user is authenticated."""
    permission_denied_message = _('You are not logged in! Please log in.')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, self.permission_denied_message)
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
