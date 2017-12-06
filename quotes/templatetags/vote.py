from django import template
from quotes.models import QuoteVote

register = template.Library()


@register.simple_tag(takes_context=True)
def vote_for(context, user, quote):
    try:
        return QuoteVote.objects.get(user=user, quote=quote)
    except QuoteVote.DoesNotExist:
        return None
