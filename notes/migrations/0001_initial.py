# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-29 14:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note_text', models.CharField(max_length=200)),
                ('note_date', models.DateTimeField(verbose_name='date created')),
            ],
        ),
        migrations.CreateModel(
            name='SimpleUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_login', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='note',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notes.SimpleUser'),
        ),
    ]