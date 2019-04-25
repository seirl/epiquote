from django.conf.urls import url
from quotes import views

urlpatterns = [
    url(r'^$', views.HomeQuotes.as_view(), name='home_quotes'),
    url(r'^last$', views.LastQuotes.as_view(), name='last_quotes'),
    url(r'^top$', views.TopQuotes.as_view(), name='top_quotes'),
    url(r'^flop$', views.FlopQuotes.as_view(), name='flop_quotes'),
    url(r'^random$', views.RandomQuotes.as_view(), name='random_quotes'),
    url(r'^search$', views.SearchQuotes.as_view(), name='search_quotes'),
    url(r'^favourites/(?P<username>.+)$', views.FavouriteQuotes.as_view(),
        name='favorite_quotes'),
    url(r'^(?P<pk>\d+)$', views.DetailQuote.as_view(), name='show_quote'),
    url(r'^add$', views.AddQuote.as_view(), name='add_quote'),
    url(r'^add_confirm$', views.AddQuoteConfirm.as_view(),
        name='add_confirm_quote'),

    url(r'^feed\.rss$', views.LatestFeed(), name='feed_quotes'),

    url(r'^(?P<quote_id>\d+)/favourite$', views.AjaxFavouriteView.as_view(),
        name='ajax_favorite_quote'),
    url(r'^(?P<quote_id>\d+)/(?P<direction>up|down)vote/?$',
        views.AjaxVoteView.as_view(),
        name='ajax_vote_quote'),
]
