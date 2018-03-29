# Generated by Django 2.0.3 on 2018-03-29 12:24

from django.conf import settings
from django.db import migrations, models


def move_favs_to_fans_mtm(apps, schema_editor):
    UserProfile = apps.get_model('quotes', 'UserProfile')
    for profile in UserProfile.objects.all():
        for quote in profile.quotes.all():
            quote.fans.add(profile.user)
            quote.save()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quotes', '0005_quotevote_manytomany'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='fans',
            field=models.ManyToManyField(related_name='favorites',
                                         to=settings.AUTH_USER_MODEL),
        ),
        migrations.RunPython(move_favs_to_fans_mtm),
    ]
