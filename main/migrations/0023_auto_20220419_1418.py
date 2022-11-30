# Generated by Django 3.2.11 on 2022-04-19 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0066_collection_management_permissions'),
        ('wagtailimages', '0023_add_choose_permissions'),
        ('main', '0022_news_is_geodev'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Miniature'),
        ),
        migrations.CreateModel(
            name='AnalyticsScriptSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('script', models.TextField(blank=True, help_text="Script d'analytics", null=True)),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.site')),
            ],
            options={
                'verbose_name': "Inscription à la lettre d'information",
            },
        ),
    ]
