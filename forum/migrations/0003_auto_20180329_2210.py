# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0002_subscribtion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.AddField(
            model_name='topic',
            name='votes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='vote',
            name='topic',
            field=models.ForeignKey(related_name='topic', to='forum.Topic'),
        ),
        migrations.AddField(
            model_name='vote',
            name='user',
            field=models.ForeignKey(related_name='vote_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
