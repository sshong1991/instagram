# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-20 08:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0006_auto_20170220_1423'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='relationship',
            unique_together=set([('from_user', 'to_user')]),
        ),
    ]