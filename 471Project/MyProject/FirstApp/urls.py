from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.homePage, name='homePage'),
    path('topArtists/', views.topArtistsPage, name ='topArtistsPage'),
    path('artist/<int:artist_id>', views.artistPage, name='artistPage'),
    path('producer/<int:producer_id>', views.producerPage, name='producerPage'),
    path('giveSongRating', views.giveSongRating, name='giveSongRating'),
    path('giveAlbumRating', views.giveAlbumRating, name='giveAlbumRating'),
    path('topAlbums/', views.topAlbumsPage, name ='topAlbumsPage'),
    path('topSongs/', views.topSongsPage, name ='topSongsPage'),
    path('login/', auth_views.LoginView.as_view(template_name="login.html", next_page="/"), name ='login'),
    path('logout/', auth_views.LogoutView.as_view(), name = 'logout'),
    path('user/<str:username>', views.userPage, name ='userPage'),
    path('song/', views.singleSongPage, name ='songPage'),
    path('album/', views.singleAlbumPage, name ='albumPage'),
    path('giveReview/', views.giveReview, name='giveReviewPage'),
    path('search/', views.search, name='searchPage'),
    path('register/', views.register, name='registerPage'),
    path('review/', views.review, name='reviewPage')
]