# Generated by Django 3.2.16 on 2022-12-06 15:58

from django.db import migrations, models
import django.db.models.deletion
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0024_index_image_file_hash'),
        ('mangmap', '0003_auto_20221206_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='platform_block_cta',
            field=models.CharField(blank=True, default='Voir la plateforme', max_length=32, verbose_name='Text du bouton'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='platform_block_description',
            field=wagtail.fields.RichTextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='platform_block_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Image'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='platform_block_title',
            field=models.CharField(blank=True, default='Notre plateforme', max_length=64, verbose_name='Titre'),
        ),
    ]
