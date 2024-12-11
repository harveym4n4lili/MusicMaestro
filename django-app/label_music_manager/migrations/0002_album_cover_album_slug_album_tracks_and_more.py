# Generated by Django 5.1.2 on 2024-12-01 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('label_music_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='album',
            name='slug',
            field=models.SlugField(default='', editable=False, max_length=512, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='album',
            name='tracks',
            field=models.ManyToManyField(related_name='albums', through='label_music_manager.AlbumTrackListItem', to='label_music_manager.song'),
        ),
        migrations.AlterField(
            model_name='album',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='album',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.AlterUniqueTogether(
            name='album',
            unique_together={('title', 'artist', 'format')},
        ),
    ]
