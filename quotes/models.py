#!/usr/bin/env python2
# -*- encoding: utf-8 -*-


from django.db import models
from django.contrib.auth.models import User


class Quote(models.Model):
    author = models.CharField(max_length=50, verbose_name='auteur')
    context = models.TextField(verbose_name='contexte', blank=True)
    content = models.TextField(verbose_name='contenu')
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, blank=True)
    votes_up = models.IntegerField(default=0)
    votes_down = models.IntegerField(default=0)
    rank = models.FloatField(default=0)
    visible = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False, verbose_name=u'accepté')
