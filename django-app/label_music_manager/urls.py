# Use this file to specify your subapp's routes
from django.urls import path, include
from . import views

from .views import BOPAlbumListView, BOPAlbumSingleView, BOPAlbumCreateView, BOPAlbumEditView, BOPAlbumDeleteView
from .views import LoginView, LogoutRequest

from. api_views import APIEndppointListView
from .api_views import AlbumListView, AlbumSingleView, TrackListView
from .api_views import SongListView, SongSingleView, TrackSingleView

urlpatterns = [
    path('accounts/login/', LoginView.as_view(), name='login-view'),
    path('accounts/logout/', views.LogoutRequest, name='logout'),
    
    
    path('', BOPAlbumListView.as_view(), name='album-list-BOP'),
    path('albums/new/', BOPAlbumCreateView.as_view(), name='album-create-BOP'),
    path('albums/<int:pk>/delete/', BOPAlbumDeleteView.as_view(), name='album-delete-BOP'),
    path('albums/<int:id>/edit/', BOPAlbumEditView.as_view(), name='album-edit-BOP'),
    path('albums/<int:id>/<slug:slug>/', BOPAlbumSingleView.as_view(), name='album-view-BOP'),
    path('albums/<int:id>/', BOPAlbumSingleView.as_view(), name='album-view-BOP'),

    
    path('api/', APIEndppointListView.as_view(), name='api-list'),
    path('api/albums/', AlbumListView.as_view(), name='album-list'),
    path('api/albums/<int:pk>/', AlbumSingleView.as_view(), name='album-view'),
    
    path('api/songs/', SongListView.as_view(), name='song-list'),
    path('api/songs/<int:pk>/', SongSingleView.as_view(), name='song-view'),
    
    path('api/tracklist/', TrackListView.as_view(), name='tracklist-list'),
    path('api/tracklist/<int:pk>/', TrackSingleView.as_view(), name='tracklist-view')
]
