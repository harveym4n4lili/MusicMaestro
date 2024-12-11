# Write your models here
from django.db import models
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from datetime import date



def generate_slug(instance):
    slug = slugify(instance.title)
    if Album.objects.filter(slug=slug).exists():
        slug = f"{slug}-{instance.id}"
    return slug

class Album(models.Model):
    FORMATS = [
        ('DD', 'Digital Download'),
        ('CD', 'Compact Disk'),
        ('VL', 'Vinyl')
    ]
    
    cover = models.ImageField(blank=True, null=True)
    title = models.CharField(max_length=512)
    description = models.TextField(blank=True, null=True)
    artist = models.CharField(max_length=512)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    format = models.CharField(max_length=2, choices=FORMATS)
    release_date = models.DateField()
    slug = models.SlugField(max_length=512, unique=True, editable=False)
    
    tracks = models.ManyToManyField(
        'Song',
        through='AlbumTracklistItem',
        related_name='albums'
    )
    
    # some constraints
    class Meta:
        unique_together = ('title', 'artist', 'format')
    
    # some validation
    def save(self, *args, **kwargs):
        # price constraints
        if self.price < 0 or self.price > 999.99:
            raise ValidationError("Price must be between 0 and 999.99 GBP.")
        
        #date constraint
        if self.release_date > date.today():
            raise ValidationError("Release date cannot be in the future.")
        
        # slug
        if not self.slug:
            self.slug = generate_slug(self)
        
        #set default cover image if not provided
        if not self.cover:
            self.cover = 'no_cover.jpg'
            
        super().save(*args, **kwargs)

    @property
    def release_year(self):
        return self.release_date.year
    
    def __str__(self):
        return f"{self.title} by {self.artist}"

class Song(models.Model):
    title = models.CharField(max_length=512)
    runningTime = models.PositiveIntegerField()
    
    
    
    def __str__(self):
        return self.title

class AlbumTrackListItem(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    position = models.PositiveIntegerField(blank=True, null=True)
    
    class Meta:
        ordering = ['position']
    
    def __str__(self):
        return f"{self.position}: {self.song.title} in {self.album.title}"

class MusicManagerUser(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    display_name = models.CharField(max_length=512, default='')
    role = models.CharField(
        max_length=10,
        choices=[
            ('artist', 'Artist'),
            ('editor', 'Editor'),
            ('viewer', 'Viewer')
        ],
        default='viewer'
    )
    
    def __str__(self):
        return self.display_name
    
