from epiquote.forms import UserRegistrationForm
from registration.backends.hmac.views import RegistrationView


class UserRegistrationView(RegistrationView):
    form_class = UserRegistrationForm
