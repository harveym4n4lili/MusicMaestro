# Write your serialisers here

from rest_framework import serializers
from .models import Album, Song, AlbumTrackListItem

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'title', 'runningTime']

class AlbumTrackListItemSerializer(serializers.ModelSerializer):
    song = SongSerializer()
    album = serializers.StringRelatedField()
    
    class Meta:
        model = AlbumTrackListItem
        fields = ['id', 'album', 'song', 'position']
        
class AlbumTrackListItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumTrackListItem
        fields = ['album', 'song', 'position']

class AlbumSerializer(serializers.ModelSerializer):
    tracks = AlbumTrackListItemWriteSerializer(source='albumtracklistitem_set', many=True, read_only=True)
    
    class Meta:
        model = Album
        fields = ['id','cover', 'description','title', 'artist', 'price', 'release_date', 'tracks']