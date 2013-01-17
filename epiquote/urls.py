from django.conf.urls import patterns, include, url
from django.contrib import admin
from voting.views import vote_on_object
from quotes.models import Quote
from quotes import views

admin.autodiscover()

quote_dict = {
    'model': Quote,
    'template_object_name': 'quote',
    'slug_field': 'id',
    'allow_xmlhttprequest': 'true',
}

urlpatterns = patterns('',
    url(r'^$', views.last_quotes),
    url(r'^last$', views.last_quotes),
    url(r'^last/(\d+)$', views.last_quotes),
    url(r'^random$', views.random_quotes),
    url(r'^search$', views.search_quotes),
    url(r'^add$', views.add_quote),
    url(r'^add_confirm$', views.add_confirm),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/register/$', 'registration.views.register',
        {
            'backend': 'quotes.views.Backend',
            'form_class': views.UserRegistrationForm
        }),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^(?P<object_id>[-\w]+)/(?P<direction>up|down|clear)vote/?$',
        vote_on_object, quote_dict, name="quote-voting"),
)
