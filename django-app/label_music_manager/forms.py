# If you require forms, write them here
from django import forms
from .models import Album, Song

class AlbumForm(forms.ModelForm):
    songs = forms.ModelMultipleChoiceField(
        queryset=Song.objects.all(), 
        required=False, 
        widget=forms.CheckboxSelectMultiple
    )
    
    class Meta:
        model = Album
        fields = ['title', 'artist', 'price', 'format', 'release_date', 'description', 'cover', 'songs']
        
