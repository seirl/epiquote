from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django_registration.backends.activation.views import RegistrationView

from epiquote.forms import UserRegistrationForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'accounts/register/',
        RegistrationView.as_view(form_class=UserRegistrationForm),
        name='register',
    ),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('comments/', include('django_comments.urls')),
    path('', include('quotes.urls')),
]

if settings.ENABLE_EPITA_CONNECT:
    urlpatterns += [
        path('accounts/', include('social_django.urls', namespace='social')),
    ]
