#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from models import Quote
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django import forms
import shlex


class SearchForm(forms.Form):
    q = forms.CharField()

    def clean_q(self):
        q = self.cleaned_data['q']
        if len(q.split()) > 30:
            raise forms.ValidationError("Trop de mots.")
        if len(q) > 300:
            raise forms.ValidationError("Trop de lettres.")
        return q


def template_processor(request):
    return {
        'quotes_search_form': SearchForm(),
    }


def get_quotes(only_visible=True, order='-date'):
    quotes = Quote.objects.order_by(order).filter(beta=False,
            visible=only_visible)
    return quotes


def split_quotes(quotes, page=0, number=30):
    return quotes[page * number: (page + 1) * number]


def last_quotes(request, page='0'):
    page = int(page)
    quotes = split_quotes(get_quotes(), page=page)
    return render(request, 'simple.html', {'name_page': 'Dernières citations',
        'quotes': quotes})


def random_quotes(request):
    quotes = split_quotes(get_quotes(order='?'))
    return render(request, 'simple.html', {'name_page':
        'Citations aléatoires', 'quotes': quotes})


def all_quotes(request):
    quotes = get_quotes()
    return render(request, 'simple.html', {'name_page':
        'Toutes les citations', 'quotes': quotes})


def search_quotes(request):
    if 'q' not in request.GET:
        raise Exception
    else:
        quotes = get_quotes()
        query = map(lambda s: u' {0} '.format(s.decode('utf-8')),
                shlex.split(request.GET['q'].encode('utf-8')))
        for w in query:
            f = (Q(content__icontains=w)
               | Q(context__icontains=w)
               | Q(author__icontains=w))
            quotes = quotes.filter(f)
        return render(request, 'simple.html', {'name_page':
            u'Recherche : {0}'.format(request.GET['q']), 'quotes': quotes})


@login_required
def add_quote(request):
    pass
