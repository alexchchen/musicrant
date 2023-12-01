from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.homePage, name='homePage'),
    path('topArtists/', views.topArtistsPage, name ='topArtistsPage'),
    path('artist/<int:artist_id>', views.artistPage, name='artistPage'),
    path('producer', views.producerPage, name='producerPage'),
    path('giveRating', views.giveRating, name='giveRating'),
    path('topAlbums/', views.topAlbumsPage, name ='topAlbumsPage'),
    path('topSongs/', views.topSongsPage, name ='topSongsPage'),
    path('login/', auth_views.LoginView.as_view(template_name="login.html", next_page="/"), name ='login'),
    path('user/', views.userPage, name ='userPage'),
    path('singleSong/', views.singleSongPage, name ='singleSongPage'),
    path('singleAlbum/', views.singleAlbumPage, name ='singleAlbumPage'),
    path('giveReview/', views.giveReview, name='giveReviewPage'),
    path('search/', views.search, name='searchPage'),
    path('register/', views.register, name='registerPage'),
    path('reviewPage/', views.review, name='reviewPage')
]