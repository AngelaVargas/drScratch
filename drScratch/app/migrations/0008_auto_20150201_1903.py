# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20150201_1604'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mastery',
            old_name='scoring',
            new_name='points',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='score',
            new_name='points',
        ),
    ]
