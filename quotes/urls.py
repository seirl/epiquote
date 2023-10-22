from django.urls import path, re_path
from quotes import views

urlpatterns = [
    path('', views.HomeQuotes.as_view(), name='home_quotes'),
    path('last', views.LastQuotes.as_view(), name='last_quotes'),
    path('top', views.TopQuotes.as_view(), name='top_quotes'),
    path('flop', views.FlopQuotes.as_view(), name='flop_quotes'),
    path('random', views.RandomQuotes.as_view(), name='random_quotes'),
    path('search', views.SearchQuotes.as_view(), name='search_quotes'),
    path(
        'favourites/<path:username>',
        views.FavouriteQuotes.as_view(),
        name='favorite_quotes',
    ),
    path('<int:pk>', views.DetailQuote.as_view(), name='show_quote'),
    path('add', views.AddQuote.as_view(), name='add_quote'),
    path(
        'add_confirm', views.AddQuoteConfirm.as_view(), name='add_confirm_quote'
    ),
    re_path(r'^feed\.rss$', views.LatestFeed(), name='feed_quotes'),
    path(
        '<int:quote_id>/favourite',
        views.AjaxFavouriteView.as_view(),
        name='ajax_favorite_quote',
    ),
    re_path(
        r'^(?P<quote_id>\d+)/(?P<direction>up|down)vote/?$',
        views.AjaxVoteView.as_view(),
        name='ajax_vote_quote',
    ),
]
