from quotes.models import Quote
from django.views.generic import ListView, DetailView


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


class QuoteDetailView(DetailView):
    context_object_name = 'quote'
    model = Quote

    def get_queryset(self):
        return Quote.objects.seen_by(self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['quotes'] = [ctx['quote']]  # for table iteration
        return ctx
