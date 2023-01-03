# Generated by Django 3.2.16 on 2023-01-03 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mangmap', '0016_auto_20221219_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='structuresettings',
            name='linkedin',
            field=models.URLField(blank=True, help_text='URL de votre page LinkedIn', null=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='introduction_youtube_video_id',
            field=models.CharField(blank=True, help_text="Indiquer ici seulement l'id de la video youtube, celui-ci est indiqué dans l'url après 'v='.             Exemple : pour https://www.youtube.com/watch?v=r3pQdvIHYBE renseigner r3pQdvIHYBE", max_length=15, null=True, verbose_name='Vidéo Youtube (id)'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='platform_block_image',
            field=models.ForeignKey(blank=True, help_text="Elle n'est utilisée que si aucune vidéo n'est renseignée", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='mangmap.customimage', verbose_name='Image'),
        ),
    ]
