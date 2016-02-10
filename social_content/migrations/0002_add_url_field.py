# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_content', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='socialaccount',
            options={'ordering': ('identifier', 'social_content_type'), 'verbose_name': 'Social Account'},
        ),
        migrations.AlterModelOptions(
            name='socialpost',
            options={'ordering': ('-created',), 'verbose_name': 'Social Post'},
        ),
        migrations.AddField(
            model_name='socialaccount',
            name='url',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='socialaccount',
            name='social_content_type',
            field=models.CharField(db_index=True, max_length=255, verbose_name=b'Type', choices=[(b'facebook', b'Facebook'), (b'twitter', b'Twitter'), (b'instagram', b'Instagram'), (b'youtube', b'YouTube'), (b'vine', b'Vine'), (b'google_plus', b'Google Plus')]),
        ),
        migrations.AlterField(
            model_name='socialpost',
            name='social_content_type',
            field=models.CharField(db_index=True, max_length=255, verbose_name=b'Type', choices=[(b'facebook', b'Facebook'), (b'twitter', b'Twitter'), (b'instagram', b'Instagram'), (b'youtube', b'YouTube'), (b'vine', b'Vine'), (b'google_plus', b'Google Plus')]),
        ),
    ]
