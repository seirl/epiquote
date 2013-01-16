#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from models import Quote
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django import forms
from django.http import Http404, HttpResponseRedirect
import shlex

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
    content = forms.CharField(widget=forms.Textarea, label="")


def template_processor(request):
    return {
        'quotes_search_form': SearchForm(),
    }


def get_quotes(only_visible=True, order='-date'):
    quotes = Quote.objects.order_by(order).filter(accepted=True)
    if only_visible:
        quotes.filter(visible=True)
    return quotes


def split_quotes(quotes, page=0, number=NUMBER_PER_PAGE):
    return quotes[page * number: (page + 1) * number]


def last_quotes(request, page=0):
    if 'p' in request.GET:
        return HttpResponseRedirect('/last/{0}'.format(request.GET['p']))
    page = int(page)
    all_quotes = get_quotes()
    max_page = len(all_quotes) / NUMBER_PER_PAGE
    if page < 0 or page > max_page:
        raise Http404()
    next_page = None if page >= max_page else page + 1
    prev_page = None if page <= 0 else page - 1
    quotes = split_quotes(all_quotes, page=page)
    return render(request, 'last.html', {'name_page': 'Dernières citations',
        'quotes': quotes, 'next_page': next_page, 'prev_page': prev_page,
        'page': page, 'max_page': max_page})


def random_quotes(request):
    quotes = split_quotes(get_quotes(order='?'))
    return render(request, 'simple.html', {'name_page':
        'Citations aléatoires', 'quotes': quotes})


def search_quotes(request):
    f = SearchForm(request.GET)
    if not f.is_valid():
        raise Http404()
    query = f.cleaned_data['q']
    quotes = get_quotes()
    terms = map(lambda s: r'(^|[^\w]){0}([^\w]|$)'.format(s.decode('utf-8')),
            shlex.split(query.encode('utf-8')))
    f = Q()
    for w in terms:
        f |= (Q(content__regex=w)
                | Q(context__regex=w)
                | Q(author__regex=w))

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
