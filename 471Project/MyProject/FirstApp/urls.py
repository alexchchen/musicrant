from django.urls import path
from . import views

urlpatterns = [
    path('FirstApp/', views.FirstView, name='FirstView'),
    path('', views.homePage, name='homePage'),
    path('topArtists/', views.topArtistsPage, name ='topArtistsPage'),
    path('FirstApp/profile/<username>', views.profile, name='profile'),
    path('artist', views.artistPage, name='artistPage'),
    path('producer', views.producerPage, name='producerPage'),
    path('giveRating', views.giveRating, name='giveRating')
]