# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-02 05:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instaapp', '0010_auto_20160701_0941'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
