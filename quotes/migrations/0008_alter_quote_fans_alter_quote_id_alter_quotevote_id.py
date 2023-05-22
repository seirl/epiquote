# Generated by Django 4.2.1 on 2023-05-22 20:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quotes', '0007_remove_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='fans',
            field=models.ManyToManyField(blank=True, related_name='favorites', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='quote',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='quotevote',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
