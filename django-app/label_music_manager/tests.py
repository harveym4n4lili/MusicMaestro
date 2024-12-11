# Write your tests here. Use only the Django testing framework.
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
from rest_framework import status
from .models import Album, MusicManagerUser

class TestMusicManager(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testUser', password='123')
        self.artistUser = User.objects.create_user(username='artistUser', password='password123')
        MusicManagerUser.objects.create(user=self.user, display_name='John Doe', role='editor')
        MusicManagerUser.objects.create(user=self.artistUser, display_name='The Band', role='artist')
    
        self.album = Album.objects.create(
            title="Test Album", 
            artist="Test Artist", 
            description = "This test album will be used to test for correct functionality.",
            price=10.99, 
            format="CD", 
            release_date=date(2023, 5, 3)
        )
        
        self.album_url = reverse('album-view', args=[self.album.id])
    
    # test for album list view
    def testAlbumList(self):
        response = self.client.get(reverse('album-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    # test for album single view 
    def testAlbumSingle(self):
        response = self.client.get(self.album_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.album.title)
        self.assertContains(response, self.album.artist)
