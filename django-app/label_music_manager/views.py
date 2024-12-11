# Use this file for your templated views only
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Album, Song, AlbumTrackListItem
from django.core.exceptions import ValidationError
from .forms import AlbumForm

# bop view for list of albums
class BOPAlbumListView(View):
    def get(self, request):
        # get logged in user
        user = request.user
        
        if user.is_authenticated and user.musicmanageruser.role == 'artist':
            # get only albums associated with ogged in user
            albums = Album.objects.filter(artist=user.musicmanageruser.display_name)
        else:
            albums = Album.objects.all()
            
        return render(request, 'albums/album_list.html', {'albums': albums})
# bop view for single album
class BOPAlbumSingleView(View):
    def get(self, request, id, slug=None):
        album = get_object_or_404(Album, pk=id)
 
        if slug and album.slug != slug:
            return redirect('album-view-BOP', id=album.id, slug=album.slug)
        
        if not slug:
            return redirect('album-view-BOP', id=album.id, slug=album.slug)
        
        # get tracks by ordered position
        tracks = AlbumTrackListItem.objects.filter(album=album).select_related('song').order_by('position')

        return render(request, 'albums/album_single.html', {'album': album, 'tracks': tracks})
# bop view for creating album
class BOPAlbumCreateView(View):
    def get(self, request):
        form = AlbumForm()
        return render(request, 'albums/album_form.html', {'form': form})

    def post(self, request):
        if not request.user.musicmanageruser.role == 'editor':
            messages.error(request, "You don't have permission to Create/Edit Albums.")
            return redirect('album-list-BOP')
        
        form = AlbumForm(request.POST)
        
        try:
            if form.is_valid():
                album = form.save()
                
                if 'clearCover' in request.POST:
                    album.cover = None
                
                # get selected songs from form
                selectedSongs = form.cleaned_data.get('songs')
                position = 1 # starting position for first song
                
                for song in selectedSongs:
                    AlbumTrackListItem.objects.create(album=album, song=song, position=position)
                    position += 1
                
                messages.success(request, f"{album.title} added successfully!")
                return redirect('album-list-BOP')
        
        except ValidationError as e:
            messages.error(request, f"Database error: {e}")
            return render(request, 'albums/album_form.html', {'form': form})
        
        print(form.errors) 
        return render(request, 'albums/album_form.html', {'form': form})

#bop view for editing album
class BOPAlbumEditView(View):
    def get(self, request, id):
        album = get_object_or_404(Album, pk=id)
        form = AlbumForm(instance=album)
        
        if album.albumtracklistitem_set.all().select_related('song').exists():
            # preselect songs already linked to album
            selectedSongs = album.albumtracklistitem_set.all().select_related('song')
            
            form.fields['songs'].initial = [item.song for item in selectedSongs]
        
        return render(request, 'albums/album_form.html', {'form': form, 'album':album})
    
    def post(self, request, id):
        album = get_object_or_404(Album, pk=id)
        form = AlbumForm(request.POST, request.FILES,instance=album)
        if form.is_valid():
            # when clear checked
            if 'clearCover' in request.POST:
                album.cover = None
                
              # get selected songs from form
            selectedSongs = form.cleaned_data.get('songs')
            position = 1 # starting position for first song
            
            # firstly clear existin tracklist entries for this album
            AlbumTrackListItem.objects.filter(album=album).delete()
            
            for song in selectedSongs:
                AlbumTrackListItem.objects.create(album=album, song=song, position=position)
                position += 1
            
            form.save()
            messages.success(request, f"{album.title} updated successfully!")
            return redirect('album-list-BOP')
        
        # form invalid message handled in template
        print(form.errors) 
        
        return render(request, 'albums/album_form.html', {'form': form, 'album': album})

#bop view for deleting album
class BOPAlbumDeleteView(View):
    def get(self, request, pk):
        album = get_object_or_404(Album, pk=pk)
        
        return render(request, 'albums/album_delete.html', {'album': album})
    
    def post(self, request, pk):
        album = get_object_or_404(Album, pk=pk)

        messages.success(request, f'Album "{album.title}" has been successfully deleted.')
        album.delete()
        
        return redirect('album-list-BOP')

# login view
class LoginView(View):
    def get(self, request):
        return render(request, 'registration/login.html')
    
    def post(self, request):
        # authenticate
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Successfully logged in as {user.username}!")
            return redirect('home')
        else:
            return render(request, 'registration', {'error': 'Incorrect username or password.'})
    
def LogoutRequest(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')   
    else:
        return redirect('login')
    