# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('membership_started', models.DateField(db_index=True, null=True, blank=True)),
                ('membership_ended', models.DateField(db_index=True, null=True, blank=True)),
                ('first_name', models.CharField(max_length=100, blank=True)),
                ('last_name', models.CharField(max_length=100, blank=True)),
                ('title', models.CharField(max_length=100, blank=True)),
                ('notes', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(unique=True)),
                ('treasurer_comments', models.TextField(blank=True)),
                ('comments', models.TextField(blank=True)),
                ('attendees', models.ManyToManyField(related_name='meetings', to='gastronomicus.Attendee')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Serving',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField(null=True, blank=True)),
                ('gift', models.BooleanField(default=False)),
                ('dish', models.ForeignKey(to='gastronomicus.Dish')),
                ('giver', models.ForeignKey(related_name='gifts', blank=True, to='gastronomicus.Attendee', null=True)),
                ('meeting', models.ForeignKey(to='gastronomicus.Meeting')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='meeting',
            name='servings',
            field=models.ManyToManyField(related_name='meetings', through='gastronomicus.Serving', to='gastronomicus.Dish'),
            preserve_default=True,
        ),
    ]
