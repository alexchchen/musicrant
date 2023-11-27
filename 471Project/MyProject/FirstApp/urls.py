from django.urls import path
from . import views

urlpatterns = [
    path('FirstApp/', views.FirstView, name='FirstView'),
    path('', views.homePage, name='homePage'),
    path('topArtists/', views.topArtistsPage, name ='topArtistsPage'),
    path('topAlbums/', views.topAlbumsPage, name ='topAlbumsPage'),
    path('topSongs/', views.topSongsPage, name ='topSongsPage'),
    path('login/', views.loginPage, name ='loginPage'),
    path('user/', views.userPage, name ='userPage'),
    path('singleSong/', views.singleSongPage, name ='singleSongPage'),
    path('FirstApp/profile/<username>', views.profile, name='profile')
]