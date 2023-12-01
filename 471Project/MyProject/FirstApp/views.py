from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from .models import *

@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    template = loader.get_template('profile.html')
    context = {
        'user': user,
    }
    return HttpResponse(template.render(context, request))


@login_required
def homePage(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


@login_required
def topArtistsPage(request):
    artists = Artist.objects.annotate(
        overall_score = Avg(
            (F('songs__ratings__originality_score') +
             F('songs__ratings__lyric_score') +
             F('songs__ratings__vibe_score') +
             F('songs__ratings__instrumental_score')) / 4 
        )
    ).order_by('-overall_score')[:10]

    template = loader.get_template('topArtists.html')
    context = {
        'artists': artists
    }
    return HttpResponse(template.render(context, request))


@login_required
def artistPage(request, artist_id):
    artist = Artist.objects.filter(artist_id=artist_id).annotate(
        overall_score = Avg(
            (F('songs__ratings__originality_score') +
             F('songs__ratings__lyric_score') +
             F('songs__ratings__vibe_score') +
             F('songs__ratings__instrumental_score')) / 4 
        )
    )[0]
    
    songs = Song.objects.filter(artist_id=artist_id).annotate(
        overall_score = Avg(
            (F('ratings__originality_score') +
             F('ratings__lyric_score') +
             F('ratings__vibe_score') +
             F('ratings__instrumental_score')) / 4 
        )
    )
    
    albums = Album.objects.filter(artist_id=artist_id).annotate(
        overall_score = Avg(
            (F('ratings__originality_score') +
             F('ratings__lyric_score') +
             F('ratings__vibe_score') +
             F('ratings__instrumental_score') +
             F('ratings__album_flow_score')) / 5 
        )
    )
    
    template = loader.get_template('artist.html')
    context = {
        'artist': artist,
        'songs': songs,
        'albums': albums
    }
    return HttpResponse(template.render(context, request))


@login_required
def producerPage(request):
    template = loader.get_template('producer.html')
    return HttpResponse(template.render())


@login_required
def giveRating(request):
    template = loader.get_template('giveRating.html')
    return HttpResponse(template.render())


@login_required
def topAlbumsPage(request):
    template = loader.get_template('topAlbums.html')
    return HttpResponse(template.render())


@login_required
def topSongsPage(request):
    template = loader.get_template('topSongs.html')
    return HttpResponse(template.render())


@login_required
def userPage(request):
    template = loader.get_template('user.html')
    return HttpResponse(template.render())


@login_required
def singleSongPage(request):
    template = loader.get_template('singleSong.html')
    return HttpResponse(template.render())


@login_required
def singleAlbumPage(request):
    template = loader.get_template('singleAlbum.html')
    return HttpResponse(template.render())


@login_required
def giveReview(request):
    template = loader.get_template('giveReview.html')
    return HttpResponse(template.render())


@login_required
def review(request):
    template = loader.get_template('review.html')
    return HttpResponse(template.render())


@login_required
def search(request):
    template = loader.get_template('search.html')
    return HttpResponse(template.render())