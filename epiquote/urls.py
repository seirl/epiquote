from django.conf.urls import include, url
from django.contrib import admin
from quotes.models import Quote
from quotes import views

admin.autodiscover()

quote_dict = {
    'model': Quote,
    'template_object_name': 'quote',
    'allow_xmlhttprequest': True,
    'template_name': 'quote_confirm_vote.html'
}

urlpatterns = [
    url(r'^$', views.home),
    url(r'^last$', views.LastQuotes.as_view()),
    url(r'^top$', views.TopQuotes.as_view()),
    url(r'^flop$', views.FlopQuotes.as_view()),
    url(r'^random$', views.RandomQuotes.as_view()),
    url(r'^search$', views.search_quotes),
    url(r'^favourites/(?P<username>\w+)$', views.FavouriteQuotes.as_view()),
    url(r'^(\d+)$', views.show_quote, name='show_quote'),
    url(r'^(\d+)/favourite$', views.favourite),
    url(r'^(?P<quote_id>\d+)/(?P<direction>up|down|clear)vote/?$', views.vote),
    url(r'^add$', views.add_quote),
    url(r'^add_confirm$', views.add_confirm),
    url(r'^feed\.rss$', views.LatestFeed()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/register/$', views.UserRegistrationView.as_view()),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^comments/', include('django_comments.urls')),
]
