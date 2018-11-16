from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import urls as auth_urls

from epiquote import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/register/$', views.UserRegistrationView.as_view()),
    url(r'^accounts/', include('django_registration.backends.activation.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^', include('quotes.urls')),
]
