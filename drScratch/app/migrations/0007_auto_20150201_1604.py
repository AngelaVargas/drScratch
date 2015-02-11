# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_file_docfile'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnonMastery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('abstraction', models.IntegerField()),
                ('paralel', models.IntegerField()),
                ('logic', models.IntegerField()),
                ('synchronization', models.IntegerField()),
                ('flowcontrol', models.IntegerField()),
                ('interactivity', models.IntegerField()),
                ('representation', models.IntegerField()),
                ('scoring', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AnonProject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.IntegerField()),
                ('date', models.DateField()),
                ('points', models.IntegerField()),
                ('level', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='anonmastery',
            name='myproject',
            field=models.ForeignKey(to='app.AnonProject'),
            preserve_default=True,
        ),
    ]
