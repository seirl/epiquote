from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from voting.views import vote_on_object
from quotes.models import Quote
from quotes import views

admin.autodiscover()

quote_dict = {
    'model': Quote,
    'template_object_name': 'quote',
    'allow_xmlhttprequest': True,
    'template_name': 'quote_confirm_vote.html'
}

urlpatterns = patterns('',
    url(r'^$', views.home),
    url(r'^last$', views.last_quotes),
    url(r'^last/(\d+)$', views.last_quotes),
    url(r'^top$', views.top_quotes),
    url(r'^flop$', views.flop_quotes),
    url(r'^random$', views.random_quotes),
    url(r'^search$', views.search_quotes),
    url(r'^favourites/(?P<username>\w+)$', views.favourites),
    url(r'^(\d+)$', views.show_quote),
    url(r'^(\d+)/favourite$', csrf_exempt(views.favourite)),
    url(r'^(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/?$',
        csrf_exempt(vote_on_object), quote_dict),
    url(r'^add$', views.add_quote),
    url(r'^add_confirm$', views.add_confirm),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/register/$', 'registration.views.register',
        {
            'backend': 'quotes.views.Backend',
            'form_class': views.UserRegistrationForm
        }),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
)
