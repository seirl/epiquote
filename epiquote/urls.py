from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from django_registration.backends.activation.views import RegistrationView

from epiquote.forms import UserRegistrationForm


def crash_test(request):
    if request.user.is_staff:
        raise RuntimeError("Crash test.")
    return HttpResponse(status=404)


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
    path('crashtest', crash_test),
    path('', include('quotes.urls')),
]

if settings.ENABLE_EPITA_CONNECT:
    urlpatterns += [
        path('accounts/', include('social_django.urls', namespace='social')),
    ]
