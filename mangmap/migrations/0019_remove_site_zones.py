# Generated by Django 3.2.16 on 2023-01-16 09:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mangmap', '0018_remove_homepage_key_figures_introduction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='site',
            name='zones',
        ),
    ]