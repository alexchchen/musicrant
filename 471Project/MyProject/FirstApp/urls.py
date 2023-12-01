from django.urls import path
from . import views

urlpatterns = [
    path('FirstApp/', views.FirstView, name='FirstView'),
    path('', views.homePage, name='homePage'),
    path('topArtists/', views.topArtistsPage, name ='topArtistsPage'),
    path('artist/<int:artist_id>', views.artistPage, name='artistPage'),
    path('producer', views.producerPage, name='producerPage'),
    path('giveSongRating', views.giveSongRating, name='giveSongRating'),
    path('giveAlbumRating', views.giveAlbumRating, name='giveAlbumRating'),
    path('topAlbums/', views.topAlbumsPage, name ='topAlbumsPage'),
    path('topSongs/', views.topSongsPage, name ='topSongsPage'),
    path('login/', views.loginPage, name ='loginPage'),
    path('user/', views.userPage, name ='userPage'),
    path('singleSong/', views.singleSongPage, name ='singleSongPage'),
    path('singleAlbum/<int:album_id>', views.singleAlbumPage, name ='singleAlbumPage'),
    path('FirstApp/profile/<username>/', views.profile, name='profile'),
    path('giveSongReview/', views.giveSongReview, name='giveSongReviewPage'),
    path('giveAlbumReview', views.giveAlbumReview, name='giveAlbumReviewPage'),
    path('search/', views.search, name='searchPage'),
    path('reviewPage/', views.review, name='reviewPage')
]