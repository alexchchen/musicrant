from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import User

def FirstView(request):
    users = User.objects.all().values()
    template = loader.get_template('all_users.html')
    context = {
        'users': users,
    }
    return HttpResponse(template.render(context, request))

def profile(request, username):
    user = User.objects.get(username=username)
    template = loader.get_template('profile.html')
    context = {
        'user': user,
    }
    return HttpResponse(template.render(context, request))

def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())

def homePage(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

def topArtistsPage(request):
    template = loader.get_template('topArtists.html')
    return HttpResponse(template.render())

def artistPage(request):
    template = loader.get_template('artist.html')
    return HttpResponse(template.render())

def producerPage(request):
    template = loader.get_template('producer.html')
    return HttpResponse(template.render())

def giveRating(request):
    template = loader.get_template('giveRating.html')
    return HttpResponse(template.render())

def topAlbumsPage(request):
    template = loader.get_template('topAlbums.html')
    return HttpResponse(template.render())

def topSongsPage(request):
    template = loader.get_template('topSongs.html')
    return HttpResponse(template.render())

def loginPage(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())

def userPage(request):
    template = loader.get_template('user.html')
    return HttpResponse(template.render())

def singleSongPage(request):
    template = loader.get_template('singleSong.html')
    return HttpResponse(template.render())

def singleAlbumPage(request):
    template = loader.get_template('singleAlbum.html')
    return HttpResponse(template.render())

def giveReview(request):
    template = loader.get_template('giveReview.html')
    return HttpResponse(template.render())

def review(request):
    template = loader.get_template('review.html')
    return HttpResponse(template.render())