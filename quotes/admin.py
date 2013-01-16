#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from django.contrib import admin
from models import Quote


def make_visible(modeladmin, request, queryset):
    queryset.update(visible=True)
make_visible.short_description = 'Rendre visibles'


def make_novisible(modeladmin, request, queryset):
    queryset.update(visible=False)
make_novisible.short_description = 'Rendre invisibles'


def make_accepted(modeladmin, request, queryset):
    queryset.update(accepted=True)
make_accepted.short_description = 'Accepter'


class QuoteAdmin(admin.ModelAdmin):
    list_display = ('author', 'context', 'content', 'date', 'accepted',
            'visible')
    list_filter = ('date', 'accepted')
    search_fields = ('author', 'context', 'content')
    actions = [make_visible, make_novisible, make_accepted]


admin.site.register(Quote, QuoteAdmin)
