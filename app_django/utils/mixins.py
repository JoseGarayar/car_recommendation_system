from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

class CustomLoginRequiredMixin(LoginRequiredMixin):

    def handle_no_permission(self):
        messages.error(self.request, 'Debes iniciar sesión para acceder a esta página.')
        return super().handle_no_permission()