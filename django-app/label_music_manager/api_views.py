# Use this file for your API viewsets only
# E.g., from rest_framework import ...

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse

from .models import Album, AlbumTrackListItem, Song
from .serializers import AlbumSerializer, AlbumTrackListItemSerializer, AlbumTrackListItemWriteSerializer, SongSerializer

class APIEndppointListView(APIView):
    def get(self, request):
        api_endpoints = {
            "Album List": reverse('album-list', request=request),
            "Album Single": reverse('album-view', args=[1], request=request).replace('/1/', '/<int:pk>/'),
            "Song List": reverse('song-list', request=request),
            "Song Single": reverse('song-view', args=[1], request=request).replace('/1/', '/<int:pk>/'),
            "Tracklist List": reverse('tracklist-list', request=request),
            "Tracklist Single": reverse('tracklist-view', args=[1], request=request).replace('/1/', '/<int:pk>/'),
        }
        return Response(api_endpoints)

class AlbumListView(APIView):
    def get(self, request):
        albums = Album.objects.all() #get all albums
        serializer = AlbumSerializer(albums, many=True)
        maxLength = 255
        
        albums_with_total_time_and_year = []
        
        # manually calculate total running time for each album
        for album in albums:
            # find total album run time
            totalTime = 0
            tracks = AlbumTrackListItem.objects.filter(album=album).select_related('song')
            for track in tracks.all():
                totalTime += track.song.runningTime
            
            album_data = AlbumSerializer(album).data
            
            # get year from release_date
            release_year = album.release_date.year if album.release_date else None

            # truncate description
            description = album_data.get('description', None)
            if description and len(description) > maxLength:
                album_data['description'] = description[:maxLength] + '...'
            
            album_data['total_playtime'] = totalTime
            album_data['release_year'] = release_year 
            
            
            albums_with_total_time_and_year.append(album_data)
        
        return Response(albums_with_total_time_and_year)
    
    # handle post method request API
    def post(self, request):
        serializer = AlbumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AlbumCreateView(APIView):
    def post(self, request):
        if not request.user.is_authenticated or request.user.musicmanager.role != 'editor':
            return Response({"error": "You don't have permissions to edit albums."})

        serializer = AlbumSerializer(data=request.data)
        
        if serializer.is_valid():
            album = serializer.save()
            
            # add tracks
            track_data = request.data.get('track_data', [])
            for track in track_data:
                songID = track['song_id']
                position = track['position']
                song = Song.objects.get(id=songID)
                AlbumTrackListItem.objects.create(album=album, song=song, position=position)
            
            return Response(AlbumSerializer(album).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
class AlbumSingleView(APIView):
    def get(self, reqest, pk):
        # get a single album by ID
        try:
            album = Album.objects.get(pk=pk)
            
            maxLength = 255
        
            albums_with_total_time_and_year = []
        
             # find total album run time
            totalTime = 0
            tracks = AlbumTrackListItem.objects.filter(album=album).select_related('song')
            for track in tracks.all():
                totalTime += track.song.runningTime
            
            album_data = AlbumSerializer(album).data
            
            # get year from release_date
            release_year = album.release_date.year if album.release_date else None

            # truncate description
            description = album_data.get('description', None)
            if description and len(description) > maxLength:
                album_data['description'] = description[:maxLength] + '...'
            
            album_data['total_playtime'] = totalTime
            album_data['release_year'] = release_year 
            
            
            albums_with_total_time_and_year.append(album_data)
        
        except Album.DoesNotExist:
            return Response({'detail': 'Album not found.'}, status=status.HTTP_404_NOT_FOUND)

        return Response(albums_with_total_time_and_year)
    # handle album update API
    def put(self, request, pk):
        try:
            album = Album.objects.get(pk=pk)
        except Album.DoesNotExist:
            return Response({'detail':'Album not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AlbumSerializer(album, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request, pk):
        try:
            album = Album.objects.get(pk=pk)
        except Album.DoesNotExist:
            return Response({'detail':'Album not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AlbumSerializer(album, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SongListView(APIView):
    def get(self, request):
        songs = Song.objects.all()
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)

     # handle post method request API
    def post(self, request):
        serializer = SongSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class SongSingleView(APIView):
    def get(self, reqest, pk):
        # get a single song by ID
        try:
            song = Song.objects.get(pk=pk)
        except Song.DoesNotExist:
            return Response({'detail': 'Song not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = SongSerializer(song)
        return Response(serializer.data)
    # handle song update API
    def put(self, request, pk):
        try:
            songs = Song.objects.get(pk=pk)
        except Song.DoesNotExist:
            return Response({'detail':'Song not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SongSerializer(songs, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request, pk):
        try:
            songs = Song.objects.get(pk=pk)
        except Song.DoesNotExist:
            return Response({'detail':'Song not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SongSerializer(songs, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TrackListView(APIView):
    def get(self, request):
        tracklist = AlbumTrackListItem.objects.all()
        serializer = AlbumTrackListItemSerializer(tracklist, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AlbumTrackListItemWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TrackSingleView(APIView):
    def get(self, reqest, pk):
        # get a single song by ID
        try:
            tracklist_item = AlbumTrackListItem.objects.get(pk=pk)
        except AlbumTrackListItem.DoesNotExist:
            return Response({'detail': 'Tracklist not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = AlbumTrackListItemSerializer(tracklist_item)
        return Response(serializer.data)
    # handle tracklist update API
    def put(self, request, pk):
        try:
            tracklist_item = AlbumTrackListItem.objects.get(pk=pk)
        except AlbumTrackListItem.DoesNotExist:
            return Response({'detail': 'Tracklist not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AlbumTrackListItemSerializer(tracklist_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request, pk):
        try:
            tracklist_item = AlbumTrackListItem.objects.get(pk=pk)
        except AlbumTrackListItem.DoesNotExist:
            return Response({'detail': 'Tracklist not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AlbumTrackListItemSerializer(tracklist_item, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete tracklist API
    def delete(self, request, pk):
        try:
            tracklist_item = AlbumTrackListItem.objects.get(pk=pk)
        except AlbumTrackListItem.DoesNotExist:
            return Response({'detail': 'Tracklist not found.'}, status=status.HTTP_404_NOT_FOUND)

        tracklist_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

