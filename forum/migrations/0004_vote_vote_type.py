# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_auto_20180329_2210'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='vote_type',
            field=models.CharField(default=b'u', max_length=1),
        ),
    ]
