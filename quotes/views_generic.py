from quotes.models import Quote
from django.views.generic import ListView, DetailView


class QuoteViewMixin:
    order = None
    limit = None

    def get_queryset(self):
        if hasattr(self, 'request'):
            user = self.request.user
        else:
            user = None
        qs = Quote.objects.seen_by(user)
        if self.order is not None:
            if self.order == '?':
                # Horrible workaround for this django bug:
                # https://code.djangoproject.com/ticket/26390
                qs = Quote.objects.raw(str(qs.query) + ' ORDER BY RANDOM()')
            else:
                qs = qs.order_by(self.order)
        if self.limit is not None:
            qs = qs[:self.limit]
        return qs


class QuoteListView(QuoteViewMixin, ListView):
    context_object_name = 'quotes'


class QuoteDetailView(QuoteViewMixin, DetailView):
    context_object_name = 'quote'
    model = Quote

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['quotes'] = [ctx['quote']]  # for table iteration
        return ctx
