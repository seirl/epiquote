from django import template
from quotes.models import QuoteVote

register = template.Library()


@register.simple_tag(takes_context=True)
def vote_for(context, user, quote):
    request = context.get('request')
    if hasattr(quote, 'user_vote_list') and request and user == request.user:
        if quote.user_vote_list:
            return quote.user_vote_list[0].vote
        return None
    try:
        return QuoteVote.objects.get(user=user, quote=quote).vote
    except QuoteVote.DoesNotExist:
        return None
