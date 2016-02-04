# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SocialAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('status', model_utils.fields.StatusField(default=b'active', max_length=100, verbose_name='status', no_check_for_status=True, choices=[(b'active', b'active'), (b'inactive', b'inactive')])),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, verbose_name='status changed', monitor='status')),
                ('social_content_type', models.CharField(db_index=True, max_length=255, verbose_name=b'Type', choices=[(b'facebook', b'Facebook'), (b'twitter', b'Twitter'), (b'instagram', b'Instagram')])),
                ('identifier', models.CharField(help_text=b'Twitter screenname, Facebook page id, Instagram username,\n         or Tumblr subdomain (e.g. "example" from "example.tumblr.com")', max_length=255)),
                ('raw_identifier', models.CharField(max_length=255, null=True, blank=True)),
                ('last_import_error', models.CharField(help_text=b'This gets checked when an import runs and fails with the identifier entered here.\n        Update your identifier and uncheck this to try and run it again during the next scheduled import', max_length=255, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Social Account',
            },
        ),
        migrations.CreateModel(
            name='SocialPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('status', model_utils.fields.StatusField(default=b'active', max_length=100, verbose_name='status', no_check_for_status=True, choices=[(b'active', b'active'), (b'inactive', b'inactive')])),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, verbose_name='status changed', monitor='status')),
                ('social_content_type', models.CharField(db_index=True, max_length=255, verbose_name=b'Type', choices=[(b'facebook', b'Facebook'), (b'twitter', b'Twitter'), (b'instagram', b'Instagram')])),
                ('payload', models.TextField(null=True, blank=True)),
                ('post_id', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('image', models.TextField()),
                ('url', models.CharField(max_length=255)),
                ('social_account', models.ForeignKey(related_name='social_posts', blank=True, to='social_content.SocialAccount', null=True)),
            ],
            options={
                'verbose_name': 'Social Post',
            },
        ),
        migrations.AlterUniqueTogether(
            name='socialaccount',
            unique_together=set([('social_content_type', 'identifier')]),
        ),
        migrations.AlterUniqueTogether(
            name='socialpost',
            unique_together=set([('social_content_type', 'post_id')]),
        ),
    ]
