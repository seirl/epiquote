#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from models import Quote
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.models import RequestSite, Site
from django.shortcuts import render
from registration.backends import default
from registration import signals
from registration.models import RegistrationProfile
from voting.models import Vote
import re
import itertools

NUMBER_PER_PAGE = 30


class SearchForm(forms.Form):
    q = forms.CharField()

    def clean_q(self):
        q = self.cleaned_data['q']
        if len(q.split()) > 30:
            raise forms.ValidationError("Trop de mots.")
        if len(q) > 300:
            raise forms.ValidationError("Trop de lettres.")
        return q


class AddQuoteForm(forms.Form):
    author = forms.CharField(label="Auteur")
    context = forms.CharField(label="Contexte", required=False)
    content = forms.CharField(widget=forms.Textarea(attrs={
      'style': 'width: 500px; heigth: 200px;'}), label="")


class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=8, label='Login EPITA')
    password1 = forms.CharField(widget=forms.PasswordInput(),
            label="Mot de passe")
    password2 = forms.CharField(widget=forms.PasswordInput(),
            label="Vérification du mot de passe")

    def clean_password2(self):
        if self.data['password1'] != self.data['password2']:
            raise forms.ValidationError(
                    'Les mots de passe ne correspondent pas.')
        return self.data['password1']

    def clean_username(self):
        if not re.match('^[a-zA-Z0-9_]{0,8}$', self.data['username']):
            raise forms.ValidationError("Ce login n'est pas valide.")
        if User.objects.filter(username=self.data['username']).exists():
            raise forms.ValidationError('Ce login est déjà enregistré.')
        return self.data['username']


class Backend(default.DefaultBackend):
    def register(self, request, **kwargs):
        username, password = kwargs['username'], kwargs['password1']
        email = username + '@epita.fr'
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        new_user = RegistrationProfile.objects.create_inactive_user(username,
                email, password, site)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user


def template_processor(request):
    return {
        'quotes_search_form': SearchForm(),
    }


def get_quotes(user):
    quotes = Quote.objects.filter(accepted=True)
    if not user.is_staff:
        quotes = quotes.filter(visible=True)
    return quotes


def get_quotes_by_vote(user, **kwargs):
    quotes = [x[0] for x in Vote.objects.get_top(Quote, **kwargs)]
    if not user.is_staff:
        quotes = filter(lambda x: x.visible, quotes)
    return quotes


def last_quotes(request, p=1):
    if 'p' in request.GET:
        return HttpResponseRedirect('/last/{0}'.format(request.GET['p']))
    quotes = get_quotes(request.user).order_by('-date')
    paginate = Paginator(quotes, NUMBER_PER_PAGE)
    try:
        page = paginate.page(p)
    except:
        raise Http404()
    return render(request, 'last.html', dict(
        {'name_page': 'Dernières citations', 'page': page}))


def top_quotes(request):
    quotes = get_quotes_by_vote(request.user, limit=50)
    return render(request, 'simple.html', dict(
        {'name_page': 'Meilleures citations', 'quotes': quotes}))


def flop_quotes(request):
    quotes = get_quotes_by_vote(request.user, limit=50, reversed=True)
    return render(request, 'simple.html', dict(
        {'name_page': 'Pires citations', 'quotes': quotes}))


def favourites(request, username):
    try:
        userprofile = request.user.get_profile()
    except:
        raise Http404()
    quotes = userprofile.quotes.all()
    return render(request, 'simple.html', dict(
        {'name_page': u'Favoris de {0}'.format(username), 'quotes': quotes}))


def home(request):
    last = get_quotes(request.user)[:5]
    top = [x for x, y in Vote.objects.get_top(Quote, limit=5)]
    return render(request, 'home.html', {'top': top, 'last': last})


def random_quotes(request):
    quotes = get_quotes(request.user).order_by('?')[0:NUMBER_PER_PAGE]
    return render(request, 'simple.html', {'name_page':
        'Citations aléatoires', 'quotes': quotes})


def show_quote(request, quote_id):
    try:
        quote = get_quotes(request.user).get(id=quote_id)
    except ObjectDoesNotExist:
        raise Http404()
    return render(request, 'quote.html', {'name_page':
        'Citation #{0}'.format(quote_id), 'quotes': [quote]})


def search_quotes(request):
    def quotes_split(s):
        l = map((lambda x: x.strip()), s.split('"'))
        l = [[e] if i % 2 else e.split() for i, e in enumerate(l)]
        return filter(bool, itertools.chain(*l))

    f = SearchForm(request.GET)
    if not f.is_valid():
        raise Http404()
    q = f.cleaned_data['q']
    terms = map(lambda s: ur'(^|[^\w]){0}([^\w]|$)'.format(re.escape(s)),
            quotes_split(q))
    if not terms:
        raise Http404()
    f = Q()
    for w in terms:
        f |= (Q(content__iregex=w)
                | Q(context__iregex=w)
                | Q(author__iregex=w))
    quotes = get_quotes(request.user).order_by('-date')
    quotes = quotes.filter(f)
    if not quotes:
        raise Http404()
    return render(request, 'simple.html', {'name_page':
        u'Recherche : {0}'.format(request.GET['q']), 'quotes': quotes})


@login_required
def add_quote(request):
    print type(request.user)
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
    return render(request, 'add.html', {'name_page':
        u'Ajouter une citation', 'add_form': form})


@login_required
def add_confirm(request):
    return render(request, 'add_confirm.html', {'name_page':
            'Ajouter une citation'})


@login_required
def favourite(request, quote_id):
    #if request.method != 'POST':
    #    raise Http404()
    try:
        quote = Quote.objects.get(id=int(quote_id))
    except:
        raise Http404()
    profile = request.user.get_profile()
    if quote in profile.quotes.all():
        profile.quotes.remove(quote)
    else:
        profile.quotes.add(quote)
    profile.save()
    return HttpResponse('')
