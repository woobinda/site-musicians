# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-29 19:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('musicians', '0004_auto_20160523_1525'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Video_url',
            new_name='VideoUrl',
        ),
    ]