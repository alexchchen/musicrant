from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.homePage, name='homePage'),
    path('topArtists/', views.topArtistsPage, name ='topArtistsPage'),
    path('artist/<int:artist_id>', views.artistPage, name='artistPage'),
    path('producer/', views.producerPage, name='producerPage'),
    path('giveSongRating', views.giveSongRating, name='giveSongRating'),
    path('giveAlbumRating', views.giveAlbumRating, name='giveAlbumRating'),
    path('topAlbums/', views.topAlbumsPage, name ='topAlbumsPage'),
    path('topSongs/', views.topSongsPage, name ='topSongsPage'),
    path('login/', auth_views.LoginView.as_view(template_name="login.html", next_page="/"), name ='login'),
    path('logout/', auth_views.LogoutView.as_view(), name = 'logout'),
    path('user/', views.userPage, name ='userPage'),
    path('singleSong/', views.singleSongPage, name ='singleSongPage'),
    path('singleAlbum/<int:album_id>', views.singleAlbumPage, name ='singleAlbumPage'),
    path('FirstApp/profile/<username>/', views.profile, name='profile'),
    path('giveSongReview/', views.giveSongReview, name='giveSongReviewPage'),
    path('giveAlbumReview', views.giveAlbumReview, name='giveAlbumReviewPage'),
    path('search/', views.search, name='searchPage'),
    path('register/', views.register, name='registerPage'),
    path('reviewPage/', views.review, name='reviewPage')
]