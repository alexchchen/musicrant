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
    albums = Album.objects.annotate(
        overall_score = Avg(
            (F('ratings__originality_score') + 
             F('ratings__lyric_score') +
             F('ratings__vibe_score') +
             F('ratings__instrumental_score') +
             F('ratings__album_flow_score')) / 5
        )
    ).order_by('-overall_score')[:10]
    artists = Artist.objects.raw("""
                                    SELECT a.artist_id, a.name
                                    FROM Artist AS a JOIN Album AS al ON a.artist_id = al.artist_id
                                 """)
    template = loader.get_template('topAlbums.html')
    context = {
        'albums': albums,
        'artists': artists
    }
    return HttpResponse(template.render(context, request))

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


def singleAlbumPage(request, album_id):
    template = loader.get_template('singleAlbum.html')
    return HttpResponse(template.render())


def giveReview(request):
    template = loader.get_template('giveReview.html')
    return HttpResponse(template.render())

def review(request):
    template = loader.get_template('review.html')
    return HttpResponse(template.render())