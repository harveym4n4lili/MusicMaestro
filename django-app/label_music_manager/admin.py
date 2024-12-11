from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Album, Song, AlbumTrackListItem, MusicManagerUser

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'format', 'release_date', 'price')
    search_fields = ('title', 'artist')


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'runningTime')
    search_fields = ('title',)

@admin.register(AlbumTrackListItem)
class AlbumTrackListItemAdmin(admin.ModelAdmin):
    list_display = ('album', 'song', 'position')
    
class MusicManagerUserInline(admin.StackedInline):
    model = MusicManagerUser
    can_delete = False
    verbose_name_plural = 'Music Manager User'
    fields = ['display_name', 'role']
    
@admin.register(MusicManagerUser)
class MusicManagerUserAdmin(admin.ModelAdmin):
    list_display = ['user']

class CustomUserAdmin(UserAdmin):
    inlines = [MusicManagerUserInline]
    

admin.site.unregister(User)
admin.site.register(get_user_model(), CustomUserAdmin)

