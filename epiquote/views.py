from epiquote.forms import UserRegistrationForm
from django_registration.backends.activation.views import RegistrationView


class UserRegistrationView(RegistrationView):
    form_class = UserRegistrationForm
