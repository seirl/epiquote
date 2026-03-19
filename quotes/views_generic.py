from django.db.models import Prefetch
from quotes.models import Quote, QuoteVote
from django.views.generic import ListView, DetailView


class QuoteViewMixin:
    order = None
    limit = None

    def get_queryset(self):
        if hasattr(self, 'request'):
            user = self.request.user
        else:
            user = None
        qs = Quote.objects.seen_by(user).prefetch_related('fans')
        if user and user.is_authenticated:
            qs = qs.prefetch_related(
                Prefetch(
                    'votes',
                    queryset=QuoteVote.objects.filter(user=user),
                    to_attr='user_vote_list'
                )
            )
        if self.order is not None:
            qs = qs.order_by(self.order)
        if self.limit is not None:
            qs = qs[: self.limit]
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
