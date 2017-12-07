import itertools
import re

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.syndication.views import Feed
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import Context, loader
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView

from quotes.models import Quote, QuoteVote
from quotes.forms import AddQuoteForm, UserRegistrationForm, SearchForm
from registration.backends.default.views import RegistrationView


class UserRegistrationView(RegistrationView):
    form_class = UserRegistrationForm


class QuoteListView(ListView):
    context_object_name = 'quotes'
    order = None
    limit = None

    def get_queryset(self):
        qs = Quote.objects.seen_by(self.request.user)
        if self.order is not None:
            qs = qs.order_by(self.order)
        if self.limit is not None:
            qs = qs[:self.limit]
        return qs


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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['username'] = self.kwargs['username']
        return context


def home(request):
    last = (Quote.objects.seen_by(request.user)
            .order_by('-date')[:settings.QUOTES_MAX_PAGE_HOME])
    top = (Quote.objects.seen_by(request.user)
           .order_by('-score')[:settings.QUOTES_MAX_PAGE_HOME])
    return render(request, 'home.html', {'top': top, 'last': last})


def show_quote(request, quote_id):
    quote = get_object_or_404(Quote.objects.seen_by(request.user), id=quote_id)
    return render(request, 'quote.html', {'quotes': [quote]})


def search_quotes(request):
    def quotes_split(s):
        l = map((lambda x: x.strip()), s.split('"'))
        l = [[e] if i % 2 else e.split() for i, e in enumerate(l)]
        return filter(bool, itertools.chain(*l))

    f = SearchForm(request.GET)
    if not f.is_valid():
        raise Http404()
    q = f.cleaned_data['q']
    terms = map(lambda s: r'(^|[^\w]){0}([^\w]|$)'.format(re.escape(s)),
                quotes_split(q))
    if not terms:
        raise Http404()
    f = Q()
    for w in terms:
        f &= (Q(content__iregex=w)
              | Q(context__iregex=w)
              | Q(author__iregex=w))
    quotes = Quote.objects.seen_by(request.user).order_by('-date')
    quotes = quotes.filter(f)
    if not quotes:
        raise Http404()
    return render(request, 'search_results.html',
                  {'search_terms': request.GET['q'], 'quotes': quotes})


@login_required
def add_quote(request):
    if request.method == 'POST':
        form = AddQuoteForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            quote = Quote(author=cd['author'], context=cd['context'],
                          content=cd['content'], user=request.user)
            quote.save()
            return HttpResponseRedirect('/add_confirm')
    else:
        form = AddQuoteForm()
    return render(request, 'add.html', {'add_form': form})


@login_required
def add_confirm(request):
    return render(request, 'add_confirm.html')


@csrf_exempt
@login_required
@require_http_methods(['POST'])
def favourite(request, quote_id):
    quote = get_object_or_404(Quote.objects.seen_by(request.user),
                              id=int(quote_id))
    profile = request.user.profile
    if quote in profile.quotes.all():
        profile.quotes.remove(quote)
    else:
        profile.quotes.add(quote)
    profile.save()
    return HttpResponse('')


@csrf_exempt
@login_required
@require_http_methods(['POST'])
def vote(request, quote_id, direction):
    VOTE_DIRECTIONS = {'up': 1, 'down': -1, 'clear': 0}
    vote = VOTE_DIRECTIONS[direction]
    quote = get_object_or_404(Quote.objects.seen_by(request.user), id=quote_id)
    try:
        qv = QuoteVote.objects.get(user=request.user, quote=quote)
        if vote == 0:
            qv.delete()
        else:
            qv.vote = vote
            qv.save()
    except QuoteVote.DoesNotExist:
        qv = QuoteVote(user=request.user, quote=quote, vote=vote)
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
