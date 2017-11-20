#!/usr/bin/env python2
# -*- encoding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class QuoteManager(models.Manager):
    def seen_by(self, user=None):
        quotes = super().get_queryset().filter(accepted=True)
        if user is None or not user.is_staff:
            quotes = quotes.filter(visible=True)
        return quotes


class Quote(models.Model):
    author = models.CharField(max_length=50, verbose_name='auteur')
    context = models.TextField(verbose_name='contexte', blank=True)
    content = models.TextField(verbose_name='contenu')
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, blank=True)
    visible = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False, verbose_name=u'accepté')

    objects = QuoteManager()

    def get_absolute_url(self):
        return reverse('show_quote', args=[self.id])


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)


post_save.connect(create_user_profile, sender=User)


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        related_name='profile',
    )
    quotes = models.ManyToManyField(Quote)
