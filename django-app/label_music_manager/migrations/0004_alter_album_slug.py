# Generated by Django 5.1.2 on 2024-12-01 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('label_music_manager', '0003_alter_album_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='slug',
            field=models.SlugField(default='', editable=False, max_length=512),
        ),
    ]
