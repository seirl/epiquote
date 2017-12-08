import itertools
import re

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.syndication.views import Feed
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import Context, loader
from django.views.generic import View, TemplateView
from django.views.generic.edit import CreateView

from quotes.models import Quote, QuoteVote
from quotes.views_generic import QuoteListView, QuoteDetailView
from quotes.forms import AddQuoteForm, UserRegistrationForm, SearchForm
from registration.backends.default.views import RegistrationView

User = get_user_model()


class DetailQuote(QuoteDetailView):
    template_name = 'quote.html'


class LastQuotes(QuoteListView):
    template_name = 'last.html'
    paginate_by = settings.QUOTES_MAX_PAGE
    order = '-date'


class TopQuotes(QuoteListView):
    template_name = 'top.html'
    paginate_by = settings.QUOTES_MAX_PAGE
    order = '-score'


class FlopQuotes(QuoteListView):
    template_name = 'flop.html'
    paginate_by = settings.QUOTES_MAX_PAGE
    order = 'score'


class RandomQuotes(QuoteListView):
    template_name = 'random.html'
    limit = settings.QUOTES_MAX_PAGE
    order = '?'


class FavouriteQuotes(QuoteListView):
    template_name = 'favourites.html'
    paginate_by = settings.QUOTES_MAX_PAGE
    order = '-date'

    def get_queryset(self):
        username = self.kwargs['username']
        userprofile = get_object_or_404(User, username=username).profile
        return super().get_queryset().filter(users_favorite=userprofile)


class HomeQuotes(QuoteListView):
    template_name = 'home.html'
    context_object_name = 'last'
    limit = settings.QUOTES_MAX_PAGE_HOME
    order = '-date'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['top'] = (Quote.objects.seen_by(self.request.user)
                          .order_by('-score')[:settings.QUOTES_MAX_PAGE_HOME])
        return context


class SearchQuotes(QuoteListView):
    template_name = 'search_results.html'
    order = '-date'

    def quotes_split(self, s):
        s = map((lambda x: x.strip()), s.split('"'))
        s = [[e] if i % 2 else e.split() for i, e in enumerate(s)]
        return filter(bool, itertools.chain(*s))

    def get_search_terms(self):
        f = SearchForm(self.request.GET)
        if not f.is_valid():
            return Quote.objects.none()
        q = f.cleaned_data['q']
        return [r'(^|[^\w]){0}([^\w]|$)'.format(re.escape(s))
                for s in self.quotes_split(q)]

    def get_queryset(self):
        terms = self.get_search_terms()
        if not terms:
            return Quote.objects.none()
        f = Q()
        for w in terms:
            f &= (Q(content__iregex=w)
                  | Q(context__iregex=w)
                  | Q(author__iregex=w))
        return super().get_queryset().filter(f)


class AddQuote(LoginRequiredMixin, CreateView):
    model = Quote
    form_class = AddQuoteForm
    success_url = '/add_confirm'
    template_name = 'add.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AddQuoteConfirm(LoginRequiredMixin, TemplateView):
    template_name = 'add_confirm.html'


class UserRegistrationView(RegistrationView):
    form_class = UserRegistrationForm


class AjaxFavouriteView(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, *args, **kwargs):
        quote = get_object_or_404(Quote.objects.seen_by(self.request.user),
                                  id=int(self.kwargs['quote_id']))
        profile = self.request.user.profile
        if quote in profile.quotes.all():
            profile.quotes.remove(quote)
        else:
            profile.quotes.add(quote)
        profile.save()
        return HttpResponse('')


class AjaxVoteView(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, *args, **kwargs):
        VOTE_DIRECTIONS = {'up': 1, 'down': -1, 'clear': 0}
        vote = VOTE_DIRECTIONS[self.kwargs['direction']]
        quote = get_object_or_404(Quote.objects.seen_by(self.request.user),
                                  id=self.kwargs['quote_id'])
        try:
            qv = QuoteVote.objects.get(user=self.request.user, quote=quote)
            if vote == 0:
                qv.delete()
            else:
                qv.vote = vote
                qv.save()
        except QuoteVote.DoesNotExist:
            qv = QuoteVote(user=self.request.user, quote=quote, vote=vote)
            qv.save()
        return HttpResponse('')


class LatestFeed(Feed):
    title = 'Epiquote'
    link = '/last'
    description = 'Les dernières citations sur Epiquote'

    def items(self):
        return (Quote.objects.seen_by(None)
                .order_by('-date')[:settings.QUOTES_MAX_PAGE])

    def item_title(self, item):
        return '#{0}'.format(item.id)

    def item_description(self, item):
        t = loader.get_template('rss_description.html')
        return t.render(Context({'context': item.context,
                                 'content': item.content,
                                 'author': item.author}))
