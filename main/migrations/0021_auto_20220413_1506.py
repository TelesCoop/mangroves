# Generated by Django 3.2.11 on 2022-04-13 13:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_auto_20220413_1340'),
    ]

    operations = [
        migrations.RenameField(
            model_name='homepage',
            old_name='ressources_block_explication',
            new_name='resources_block_explication',
        ),
        migrations.RenameField(
            model_name='homepage',
            old_name='ressources_block_introduction',
            new_name='resources_block_introduction',
        ),
        migrations.RenameField(
            model_name='homepage',
            old_name='ressources_block_title',
            new_name='resources_block_title',
        ),
    ]
