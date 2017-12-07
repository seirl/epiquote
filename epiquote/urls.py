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
    url(r'^$', views.HomeQuotes.as_view()),
    url(r'^last$', views.LastQuotes.as_view()),
    url(r'^top$', views.TopQuotes.as_view()),
    url(r'^flop$', views.FlopQuotes.as_view()),
    url(r'^random$', views.RandomQuotes.as_view()),
    url(r'^search$', views.SearchQuotes.as_view()),
    url(r'^favourites/(?P<username>\w+)$', views.FavouriteQuotes.as_view()),
    url(r'^(?P<pk>\d+)$', views.DetailQuote.as_view(), name='show_quote'),
    url(r'^(\d+)/favourite$', views.favourite),
    url(r'^(?P<quote_id>\d+)/(?P<direction>up|down|clear)vote/?$', views.vote),
    url(r'^add$', views.AddQuote.as_view()),
    url(r'^add_confirm$', views.AddQuoteConfirm.as_view()),
    url(r'^feed\.rss$', views.LatestFeed()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/register/$', views.UserRegistrationView.as_view()),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^comments/', include('django_comments.urls')),
]
