from django.contrib import admin
from .models import Quote


def make_visible(modeladmin, request, queryset):
    queryset.update(visible=True)


make_visible.short_description = 'Rendre visibles'


def make_novisible(modeladmin, request, queryset):
    queryset.update(visible=False)


make_novisible.short_description = 'Rendre invisibles'


def make_accepted(modeladmin, request, queryset):
    queryset.update(accepted=True)


make_accepted.short_description = 'Accepter'


def make_visibleaccepted(modeladmin, request, queryset):
    queryset.update(visible=True, accepted=True)


make_visibleaccepted.short_description = 'Accepter et rendre visible'


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'context',
        'content',
        'date',
        'accepted',
        'visible',
    )
    list_filter = ('date', 'accepted')
    search_fields = ('author', 'context', 'content')
    actions = [
        make_visibleaccepted,
        make_visible,
        make_novisible,
        make_accepted,
    ]
