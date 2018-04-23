from django.conf.urls import include, url
from django.contrib import admin
from epiquote import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/register/$', views.UserRegistrationView.as_view()),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^', include('quotes.urls')),
]
