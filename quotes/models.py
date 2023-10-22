from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum, Count
from django.db.models.functions import Coalesce
from django.urls import reverse
from django.utils.timezone import now

User = get_user_model()


class QuoteManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                score=Coalesce(Sum('votes__vote'), 0),
                num_votes=Count('votes__vote'),
            )
        )

    def seen_by(self, user=None):
        quotes = self.get_queryset().filter(accepted=True)
        if user is None or not user.is_staff:
            quotes = quotes.filter(visible=True)
        return quotes


class Quote(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=50, verbose_name='auteur')
    context = models.TextField(verbose_name='contexte', blank=True)
    content = models.TextField(verbose_name='contenu')
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    visible = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False, verbose_name=u'accepté')

    voters = models.ManyToManyField(
        User, through='QuoteVote', related_name='voted_quotes'
    )
    fans = models.ManyToManyField(User, related_name='favorites', blank=True)

    objects = QuoteManager()

    def get_absolute_url(self):
        return reverse('show_quote', args=[self.id])


class QuoteVote(models.Model):
    SCORES = (
        (+1, '+1'),
        (-1, '-1'),
    )

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='votes'
    )
    quote = models.ForeignKey(
        Quote, on_delete=models.CASCADE, related_name='votes'
    )
    vote = models.SmallIntegerField(choices=SCORES)
    timestamp = models.DateTimeField(editable=False, default=now)

    class Meta:
        unique_together = (('user', 'quote'),)

    def __str__(self):
        return '%s: %s on %s' % (self.user, self.vote, self.quote)
