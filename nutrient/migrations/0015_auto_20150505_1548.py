# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nutrient', '0014_auto_20150505_0527'),
    ]

    operations = [
        migrations.AddField(
            model_name='nutritionfact',
            name='corroborate',
            field=models.ManyToManyField(related_name='corroborating_users', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='nutritionfact',
            name='dispute',
            field=models.ManyToManyField(related_name='disputing_users', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
