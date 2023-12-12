from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from django.db.models import Avg, Case, When, Exists, OuterRef, Value, BooleanField, Subquery
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import RegisterForm, SongRatingForm, AlbumRatingForm, SongReviewForm, AlbumReviewForm, CommentForm
from itertools import chain


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
    song_reviews = Song_Review.objects.annotate(
        overall_score =
            (F('rating_id__originality_score') +
             F('rating_id__lyric_score') +
             F('rating_id__vibe_score') +
             F('rating_id__instrumental_score')) / 4.0 
    ).annotate(
        votes = F('upvotes') - F('downvotes')
    ).order_by('-votes')[:50].annotate(
        vote_type = Case(
            When(
                Exists(
                    Upvotes_Downvotes_Song_Review.objects.filter(
                        review_id=OuterRef('review_id'),
                        username=request.user
                    )
                ),
                then=Subquery(
                    Upvotes_Downvotes_Song_Review.objects.filter(
                        review_id=OuterRef('review_id'),
                        username=request.user
                    ).values('vote_type')[:1]
                )
            ),
            default=Value(None),
            output_field=BooleanField()
        )
    )
    
    album_reviews = Album_Review.objects.annotate(
        overall_score =
            (F('rating_id__originality_score') +
             F('rating_id__lyric_score') +
             F('rating_id__vibe_score') +
             F('rating_id__instrumental_score') +
             F('rating_id__album_flow_score')) / 5.0 
    ).annotate(
        votes = F('upvotes') - F('downvotes')
    ).order_by('-votes')[:50].annotate(
        vote_type = Case(
            When(
                Exists(
                    Upvotes_Downvotes_Album_Review.objects.filter(
                        review_id=OuterRef('review_id'),
                        username=request.user
                    )
                ),
                then=Subquery(
                    Upvotes_Downvotes_Album_Review.objects.filter(
                        review_id=OuterRef('review_id'),
                        username=request.user
                    ).values('vote_type')[:1]
                )
            ),
            default=Value(None),
            output_field=BooleanField()
        )
    )        
    
    reviews = list(sorted(chain(song_reviews, album_reviews), key=lambda x: x.votes, reverse=True))
        
    template = loader.get_template('index.html')
    context = {
        'reviews': reviews
    }
    return HttpResponse(template.render(context, request))


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
def producerPage(request, producer_id):
    producer = Producer.objects.filter(producer_id=producer_id).annotate(
        overall_score = Avg(
            (F('albums_produced__songs__ratings__originality_score') +
             F('albums_produced__songs__ratings__lyric_score') +
             F('albums_produced__songs__ratings__vibe_score') +
             F('albums_produced__songs__ratings__instrumental_score') +
             F('singles_produced__ratings__originality_score') +
             F('singles_produced__ratings__lyric_score') +
             F('singles_produced__ratings__vibe_score') +
             F('singles_produced__ratings__instrumental_score')) / 8 
        )
    )[0]
    
    singles_produced = producer.singles_produced.annotate(
        overall_score = Avg(
            (F('ratings__originality_score') +
             F('ratings__lyric_score') +
             F('ratings__vibe_score') +
             F('ratings__instrumental_score')) / 4 
        )
    )
    
    albums_produced = producer.albums_produced.annotate(
        overall_score = Avg(
            (F('ratings__originality_score') +
             F('ratings__lyric_score') +
             F('ratings__vibe_score') +
             F('ratings__instrumental_score') +
             F('ratings__album_flow_score')) / 5 
        )
    )
    
    template = loader.get_template('producer.html')
    context = {
        'producer': producer,
        'singles_produced': singles_produced,
        'albums_produced': albums_produced
    }
    return HttpResponse(template.render(context, request))

@login_required
def giveSongRating(request, song_id):
    song = Song.objects.get(song_id=song_id)
    
    try:
        song_rating = Song_Rating.objects.get(username=request.user, song_id=song_id)
    except Song_Rating.DoesNotExist:
        song_rating = None
    
    if request.method == 'POST':
        form = SongRatingForm(request.POST)
        if form.is_valid():
            originality_score = int(form.cleaned_data['originality_score'])
            lyric_score = int(form.cleaned_data['lyric_score'])
            vibe_score = int(form.cleaned_data['vibe_score'])
            instrumental_score = int(form.cleaned_data['instrumental_score'])

            if song_rating is None:
                song_rating = Song_Rating(
                    username = request.user,
                    song_id = song,
                    originality_score = originality_score,
                    lyric_score = lyric_score,
                    vibe_score = vibe_score,
                    instrumental_score = instrumental_score
                )
            else:
                song_rating.originality_score = originality_score
                song_rating.lyric_score = lyric_score
                song_rating.vibe_score = vibe_score
                song_rating.instrumental_score = instrumental_score
                
            song_rating.save()
            
            messages.success(request, 'Song rating successfully given!')
    else:
        if song_rating is None:
            form = SongRatingForm()
        else:
            form = SongRatingForm(
                initial = {
                    'originality_score': song_rating.originality_score,
                    'lyric_score': song_rating.lyric_score,
                    'vibe_score': song_rating.vibe_score,
                    'instrumental_score': song_rating.instrumental_score
                }
            )
    
    template = loader.get_template('giveSongRating.html')
    context = {
        'song': song,
        'form': form
    }
    return HttpResponse(template.render(context, request))


@login_required
def giveAlbumRating(request, album_id):
    album = Album.objects.get(album_id=album_id)
    
    try:
        album_rating = Album_Rating.objects.get(username=request.user, album_id=album_id)
    except Album_Rating.DoesNotExist:
        album_rating = None
    
    if request.method == 'POST':
        form = AlbumRatingForm(request.POST)
        if form.is_valid():
            originality_score = int(form.cleaned_data['originality_score'])
            lyric_score = int(form.cleaned_data['lyric_score'])
            vibe_score = int(form.cleaned_data['vibe_score'])
            instrumental_score = int(form.cleaned_data['instrumental_score'])
            album_flow_score = int(form.cleaned_data['album_flow_score'])
            
            if album_rating is None:
                album_rating = Album_Rating(
                    username = request.user,
                    album_id = album,
                    originality_score = originality_score,
                    lyric_score = lyric_score,
                    vibe_score = vibe_score,
                    instrumental_score = instrumental_score,
                    album_flow_score = album_flow_score
                )
            else:
                album_rating.originality_score = originality_score
                album_rating.lyric_score = lyric_score
                album_rating.vibe_score = vibe_score
                album_rating.instrumental_score = instrumental_score
                album_rating.album_flow_score = album_flow_score
                
            album_rating.save()
            
            messages.success(request, 'Album rating successfully given!')
    else:
        if album_rating is None:
            form = AlbumRatingForm()
        else:
            form = AlbumRatingForm(
                initial = {
                    'originality_score': album_rating.originality_score,
                    'lyric_score': album_rating.lyric_score,
                    'vibe_score': album_rating.vibe_score,
                    'instrumental_score': album_rating.instrumental_score,
                    'album_flow_score': album_rating.album_flow_score
                }
            )
    
    template = loader.get_template('giveAlbumRating.html')
    context = {
        'album': album,
        'form': form
    }
    return HttpResponse(template.render(context, request))


@login_required
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
    artists = Artist.objects.all()
    producers = Producer.objects.all()
    template = loader.get_template('topAlbums.html')
    context = {
        'albums': albums,
        'artists': artists,
        'producers': producers
    }
    return HttpResponse(template.render(context, request))


@login_required
def topSongsPage(request):
    songs = Song.objects.annotate(
        overall_score = Avg(
            (F('ratings__originality_score') +
             F('ratings__lyric_score') +
             F('ratings__vibe_score') +
             F('ratings__instrumental_score')) / 4
        )
    ).order_by('-overall_score')[:10]
    artists = Artist.objects.all()
    producers = Producer.objects.all()
    template = loader.get_template('topSongs.html')
    context = {
        'songs': songs,
        'artists': artists,
        'producers': producers
    }
    return HttpResponse(template.render(context, request))


@login_required
def userPage(request, username):
    user = User.objects.get(username=username)
    
    song_reviews = Song_Review.objects.filter(username=user.id).annotate(
        overall_score =
            (F('rating_id__originality_score') +
             F('rating_id__lyric_score') +
             F('rating_id__vibe_score') +
             F('rating_id__instrumental_score')) / 4.0 
    ).annotate(
        votes = F('upvotes') - F('downvotes')
    ).order_by('-votes')[:50].annotate(
        vote_type = Case(
            When(
                Exists(
                    Upvotes_Downvotes_Song_Review.objects.filter(
                        review_id=OuterRef('review_id'),
                        username=request.user
                    )
                ),
                then=Subquery(
                    Upvotes_Downvotes_Song_Review.objects.filter(
                        review_id=OuterRef('review_id'),
                        username=request.user
                    ).values('vote_type')[:1]
                )
            ),
            default=Value(None),
            output_field=BooleanField()
        )
    )
    
    album_reviews = Album_Review.objects.filter(username=user.id).annotate(
        overall_score =
            (F('rating_id__originality_score') +
             F('rating_id__lyric_score') +
             F('rating_id__vibe_score') +
             F('rating_id__instrumental_score') +
             F('rating_id__album_flow_score')) / 5.0 
    ).annotate(
        votes = F('upvotes') - F('downvotes')
    ).order_by('-votes')[:50].annotate(
        vote_type = Case(
            When(
                Exists(
                    Upvotes_Downvotes_Album_Review.objects.filter(
                        review_id=OuterRef('review_id'),
                        username=request.user
                    )
                ),
                then=Subquery(
                    Upvotes_Downvotes_Album_Review.objects.filter(
                        review_id=OuterRef('review_id'),
                        username=request.user
                    ).values('vote_type')[:1]
                )
            ),
            default=Value(None),
            output_field=BooleanField()
        )
    )
    
    reviews = list(sorted(chain(song_reviews, album_reviews), key=lambda x: x.votes, reverse=True))    
    
    template = loader.get_template('user.html')
    context = {
        'user': user,
        'reviews': reviews
    }
    return HttpResponse(template.render(context, request))


@login_required
def singleSongPage(request, song_id):
    song = Song.objects.filter(song_id=song_id).annotate(
        overall_score = Avg(
            (F('ratings__originality_score') +
             F('ratings__lyric_score') +
             F('ratings__vibe_score') +
             F('ratings__instrumental_score')) / 4 
        )
    ).annotate(
        originality_score = Avg(F('ratings__originality_score')) 
    ).annotate(
        lyric_score = Avg(F('ratings__lyric_score')) 
    ).annotate(
        vibe_score = Avg(F('ratings__vibe_score')) 
    ).annotate(
        instrumental_score = Avg(F('ratings__instrumental_score')) 
    )[0]

    song_reviews = Song_Review.objects.filter(song_id=song_id).annotate(
        overall_score = 
            (F('rating_id__originality_score') +
             F('rating_id__lyric_score') +
             F('rating_id__vibe_score') +
             F('rating_id__instrumental_score')) / 4.0 
    ).annotate(
        votes = F('upvotes') - F('downvotes')
    ).order_by('-votes')[:50].annotate(
        vote_type = Case(
            When(
                Exists(
                    Upvotes_Downvotes_Song_Review.objects.filter(
                        review_id=OuterRef('review_id'),
                        username=request.user
                    )
                ),
                then=Subquery(
                    Upvotes_Downvotes_Song_Review.objects.filter(
                        review_id=OuterRef('review_id'),
                        username=request.user
                    ).values('vote_type')[:1]
                )
            ),
            default=Value(None),
            output_field=BooleanField()
        )
    )
 
    template = loader.get_template('singleSong.html')
    context = {
        'song' : song,
        'reviews': song_reviews
    }
    return HttpResponse(template.render(context, request))


@login_required
def singleAlbumPage(request, album_id):
    album = Album.objects.filter(album_id=album_id).annotate(
        album_overall_score = Avg(
            (F('ratings__originality_score') + 
             F('ratings__lyric_score') +
             F('ratings__vibe_score') +
             F('ratings__instrumental_score') + 
             F('ratings__album_flow_score')) / 5  
        )
    ).annotate(
        originality_score = Avg(F('ratings__originality_score'))
    ).annotate(
        lyric_score = Avg(F('ratings__lyric_score'))
    ).annotate(
        vibe_score = Avg(F('ratings__vibe_score'))
    ).annotate(
        instrumental_score = Avg(F('ratings__instrumental_score'))
    ).annotate(
        album_flow_score = Avg('ratings__album_flow_score')
    )[0]

    songs = Song.objects.filter(album_id=album_id)

    reviews = Album_Review.objects.filter(album_id=album_id).annotate (
        overall_score = 
        (F('rating_id__originality_score') +
         F('rating_id__lyric_score') +
         F('rating_id__vibe_score') +
         F('rating_id__instrumental_score') +
         F('rating_id__instrumental_score')) / 5.0
    ).annotate(
        votes = F('upvotes') - F('downvotes')
    ).order_by('-votes')[:50].annotate(
        vote_type = Case(
            When(
                Exists(
                    Upvotes_Downvotes_Album_Review.objects.filter(
                        review_id=OuterRef('review_id'),
                        username=request.user
                    )
                ),
                then=Subquery(
                    Upvotes_Downvotes_Album_Review.objects.filter(
                        review_id=OuterRef('review_id'),
                        username=request.user
                    ).values('vote_type')[:1]
                )
            ),
            default=Value(None),
            output_field=BooleanField()
        )
    )
    
    template = loader.get_template('singleAlbum.html')
    context = {
        'album': album,
        'reviews': reviews,
        'songs' : songs
    }
    return HttpResponse(template.render(context, request))


@login_required
def giveSongReview(request, song_id):
    song = Song.objects.get(song_id=song_id)
    
    try:
        song_rating = Song_Rating.objects.get(username=request.user, song_id=song_id)
    except Song_Rating.DoesNotExist:
        song_rating = None
        
    try:
        song_review = Song_Review.objects.get(username=request.user, song_id=song_id)
    except Song_Review.DoesNotExist:
        song_review = None
        
    if request.method == 'POST':
        rating_form = SongRatingForm(request.POST)
        review_form = SongReviewForm(request.POST, auto_id=True)
        if rating_form.is_valid() and review_form.is_valid():
            originality_score = int(rating_form.cleaned_data['originality_score'])
            lyric_score = int(rating_form.cleaned_data['lyric_score'])
            vibe_score = int(rating_form.cleaned_data['vibe_score'])
            instrumental_score = int(rating_form.cleaned_data['instrumental_score'])
            
            if song_rating is None:
                song_rating = Song_Rating(
                    username = request.user,
                    song_id = song,
                    originality_score = originality_score,
                    lyric_score = lyric_score,
                    vibe_score = vibe_score,
                    instrumental_score = instrumental_score
                )
            else:
                song_rating.originality_score = originality_score
                song_rating.lyric_score = lyric_score
                song_rating.vibe_score = vibe_score
                song_rating.instrumental_score = instrumental_score
                
            song_rating.save()
            
            title = review_form.cleaned_data['title']
            body = review_form.cleaned_data['body']
            
            if song_review is None:
                song_review = Song_Review(
                    username = request.user,
                    song_id = song,
                    rating_id = song_rating,
                    title = title,
                    body = body
                )
            else:
                song_review.rating_id = song_rating
                song_review.title = title
                song_review.body = body
                
            song_review.save()
                
            return redirect('songReviewPage', review_id=song_review.review_id)
    
    else:
        if song_rating is None:
            rating_form = SongRatingForm()
        else:
            rating_form = SongRatingForm(
                initial = {
                    'originality_score': song_rating.originality_score,
                    'lyric_score': song_rating.lyric_score,
                    'vibe_score': song_rating.vibe_score,
                    'instrumental_score': song_rating.instrumental_score
                }
            )
        if song_review is None:
            review_form = SongReviewForm(auto_id=True)
        else:
            review_form = SongReviewForm(
                auto_id = True,
                initial = {
                    'title': song_review.title,
                    'body': song_review.body
                }
            )
    
    template = loader.get_template('giveSongReview.html')
    context = {
        'song': song,
        'rating_form': rating_form,
        'review_form': review_form
    }
    return HttpResponse(template.render(context, request))


@login_required
def giveAlbumReview(request, album_id):
    album = Album.objects.get(album_id=album_id)
    
    try:
        album_rating = Album_Rating.objects.get(username=request.user, album_id=album_id)
    except Album_Rating.DoesNotExist:
        album_rating = None
        
    try:
        album_review = Album_Review.objects.get(username=request.user, album_id=album_id)
    except Album_Review.DoesNotExist:
        album_review = None
        
    if request.method == 'POST':
        rating_form = AlbumRatingForm(request.POST)
        review_form = AlbumReviewForm(request.POST, auto_id=True)
        if rating_form.is_valid() and review_form.is_valid():
            originality_score = int(rating_form.cleaned_data['originality_score'])
            lyric_score = int(rating_form.cleaned_data['lyric_score'])
            vibe_score = int(rating_form.cleaned_data['vibe_score'])
            instrumental_score = int(rating_form.cleaned_data['instrumental_score'])
            album_flow_score = int(rating_form.cleaned_data['album_flow_score'])
            
            if album_rating is None:
                album_rating = Album_Rating(
                    username = request.user,
                    album_id = album,
                    originality_score = originality_score,
                    lyric_score = lyric_score,
                    vibe_score = vibe_score,
                    instrumental_score = instrumental_score,
                    album_flow_score = album_flow_score
                )
            else:
                album_rating.originality_score = originality_score
                album_rating.lyric_score = lyric_score
                album_rating.vibe_score = vibe_score
                album_rating.instrumental_score = instrumental_score
                album_rating.album_flow_score = album_flow_score
                
            album_rating.save()
            
            title = review_form.cleaned_data['title']
            body = review_form.cleaned_data['body']
            
            if album_review is None:
                album_review = Album_Review(
                    username = request.user,
                    album_id = album,
                    rating_id = album_rating,
                    title = title,
                    body = body
                )
            else:
                album_review.rating_id = album_rating
                album_review.title = title
                album_review.body = body
                
            album_review.save()
                
            return redirect('albumReviewPage', review_id=album_review.review_id)
    
    else:
        if album_rating is None:
            rating_form = AlbumRatingForm()
        else:
            rating_form = AlbumRatingForm(
                initial = {
                    'originality_score': album_rating.originality_score,
                    'lyric_score': album_rating.lyric_score,
                    'vibe_score': album_rating.vibe_score,
                    'instrumental_score': album_rating.instrumental_score,
                    'album_flow_score': album_rating.album_flow_score
                }
            )
        if album_review is None:
            review_form = AlbumReviewForm(auto_id=True)
        else:
            review_form = AlbumReviewForm(
                auto_id = True,
                initial = {
                    'title': album_review.title,
                    'body': album_review.body
                }
            )
    
    template = loader.get_template('giveAlbumReview.html')
    context = {
        'album': album,
        'rating_form': rating_form,
        'review_form': review_form
    }
    return HttpResponse(template.render(context, request))


@login_required
def songReview(request, review_id):
    review = Song_Review.objects.filter(review_id=review_id).annotate(
        overall_score =
            (F('rating_id__originality_score') +
             F('rating_id__lyric_score') +
             F('rating_id__vibe_score') +
             F('rating_id__instrumental_score')) / 4.0
    )[0]
    
    if review.voted_users.filter(username=request.user).exists():
        vote_type = review.upvotes_downvotes_song_review_set.get(username=request.user).vote_type
    else:
        vote_type = None
        
    if request.method == 'POST':
        comment_form = CommentForm(request.POST, auto_id=True)
        if comment_form.is_valid():
            body = comment_form.cleaned_data['body']
            comment = Song_Review_Comment(
                review_id = review,
                username = request.user,
                body = body
            )
            comment.save()
            return redirect('songReviewPage', review_id=review_id)
    else:
        comment_form = CommentForm(auto_id=True)
    
    comments = review.comments.annotate(
        vote_type = Case(
            When(
                Exists(
                    Upvotes_Downvotes_Song_Review_Comment.objects.filter(
                        comment_id=OuterRef('comment_id'),
                        username=request.user
                    )
                ),
                then=Subquery(
                    Upvotes_Downvotes_Song_Review_Comment.objects.filter(
                        comment_id=OuterRef('comment_id'),
                        username=request.user
                    ).values('vote_type')[:1]
                )
            ),
            default=Value(None),
            output_field=BooleanField()
        )
    )
    
    template = loader.get_template('songReview.html')
    context = {
        'review': review,
        'comment_form': comment_form,
        'comments': comments,
        'vote_type': vote_type
    }
    return HttpResponse(template.render(context, request))


@login_required
def albumReview(request, review_id):
    review = Album_Review.objects.filter(review_id=review_id).annotate(
        overall_score =
            (F('rating_id__originality_score') +
             F('rating_id__lyric_score') +
             F('rating_id__vibe_score') +
             F('rating_id__instrumental_score') +
             F('rating_id__album_flow_score')) / 5.0
    )[0]
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST, auto_id=True)
        if comment_form.is_valid():
            body = comment_form.cleaned_data['body']
            comment = Album_Review_Comment(
                review_id = review,
                username = request.user,
                body = body
            )
            comment.save()
            return redirect('albumReviewPage', review_id=review_id)
    else:
        comment_form = CommentForm(auto_id=True)    
    
    comments = review.comments.annotate(
        vote_type = Case(
            When(
                Exists(
                    Upvotes_Downvotes_Album_Review_Comment.objects.filter(
                        comment_id=OuterRef('comment_id'),
                        username=request.user
                    )
                ),
                then=Subquery(
                    Upvotes_Downvotes_Album_Review_Comment.objects.filter(
                        comment_id=OuterRef('comment_id'),
                        username=request.user
                    ).values('vote_type')[:1]
                )
            ),
            default=Value(None),
            output_field=BooleanField()
        )
    )
    
    if review.voted_users.filter(username=request.user).exists():
        vote_type = review.upvotes_downvotes_album_review_set.get(username=request.user).vote_type
    else:
        vote_type = None
    
    template = loader.get_template('albumReview.html')
    context = {
        'review': review,
        'comment_form': comment_form,
        'comments': comments,
        'vote_type': vote_type
    }
    return HttpResponse(template.render(context, request))


@login_required
def search(request):
    query = request.GET.get('query')
    
    artists = Artist.objects.filter(Q(name__icontains=query))
    albums = Album.objects.filter(Q(name__icontains=query))
    songs = Song.objects.filter(Q(name__icontains=query))
    users = User.objects.filter(Q(username__icontains=query))
    
    template = loader.get_template('search.html')
    context = {
        'artists': artists,
        'albums': albums,
        'songs': songs,
        'users': users
    }
    return HttpResponse(template.render(context, request))


@login_required
def upvoteSongReview(request, review_id):
    review = Song_Review.objects.get(review_id=review_id)
    
    if review.voted_users.filter(username=request.user).exists():
        upvotes_downvotes_song_review = review.upvotes_downvotes_song_review_set.get(username=request.user)
        if upvotes_downvotes_song_review.vote_type == False:
            review.downvotes -= 1
            review.upvotes += 1
            review.save()
            
            upvotes_downvotes_song_review.vote_type = True
            upvotes_downvotes_song_review.save()
        else:
            review.upvotes -= 1
            review.save()
            upvotes_downvotes_song_review.delete()
    else:
        review.upvotes += 1
        review.save()
        
        upvotes_downvotes_song_review = Upvotes_Downvotes_Song_Review(
            username = request.user,
            review_id = review,
            vote_type = True
        )
        upvotes_downvotes_song_review.save()
    
    prev = request.POST.get('prev', '/')
    return redirect(prev)

@login_required
def downvoteSongReview(request, review_id):
    review = Song_Review.objects.get(review_id=review_id)
    
    if review.voted_users.filter(username=request.user).exists():
        upvotes_downvotes_song_review = review.upvotes_downvotes_song_review_set.get(username=request.user)
        if upvotes_downvotes_song_review.vote_type == True:
            review.upvotes -= 1
            review.downvotes += 1
            review.save()
            
            upvotes_downvotes_song_review.vote_type = False
            upvotes_downvotes_song_review.save()
        else:
            review.downvotes -= 1
            review.save()
            upvotes_downvotes_song_review.delete()
    else:
        review.downvotes += 1
        review.save()
        
        upvotes_downvotes_song_review = Upvotes_Downvotes_Song_Review(
            username = request.user,
            review_id = review,
            vote_type = False
        )
        upvotes_downvotes_song_review.save()
    
    prev = request.POST.get('prev', '/')
    return redirect(prev)


@login_required
def upvoteAlbumReview(request, review_id):
    review = Album_Review.objects.get(review_id=review_id)
    
    if review.voted_users.filter(username=request.user).exists():
        upvotes_downvotes_album_review = review.upvotes_downvotes_album_review_set.get(username=request.user)
        if upvotes_downvotes_album_review.vote_type == False:
            review.downvotes -= 1
            review.upvotes += 1
            review.save()
            
            upvotes_downvotes_album_review.vote_type = True
            upvotes_downvotes_album_review.save()
        else:
            review.upvotes -= 1
            review.save()
            upvotes_downvotes_album_review.delete()
    else:
        review.upvotes += 1
        review.save()
        
        upvotes_downvotes_album_review = Upvotes_Downvotes_Album_Review(
            username = request.user,
            review_id = review,
            vote_type = True
        )
        upvotes_downvotes_album_review.save()
    
    prev = request.POST.get('prev', '/')
    return redirect(prev)


@login_required
def downvoteAlbumReview(request, review_id):
    review = Album_Review.objects.get(review_id=review_id)
    
    if review.voted_users.filter(username=request.user).exists():
        upvotes_downvotes_album_review = review.upvotes_downvotes_album_review_set.get(username=request.user)
        if upvotes_downvotes_album_review.vote_type == True:
            review.upvotes -= 1
            review.downvotes += 1
            review.save()
            
            upvotes_downvotes_album_review.vote_type = False
            upvotes_downvotes_album_review.save()
        else:
            review.downvotes -= 1
            review.save()
            upvotes_downvotes_album_review.delete()
    else:
        review.downvotes += 1
        review.save()
        
        upvotes_downvotes_album_review = Upvotes_Downvotes_Album_Review(
            username = request.user,
            review_id = review,
            vote_type = False
        )
        upvotes_downvotes_album_review.save()
    
    prev = request.POST.get('prev', '/')
    return redirect(prev)


@login_required
def upvoteSongReviewComment(request, review_id, comment_id):
    review = Song_Review.objects.get(review_id=review_id)
    comment = Song_Review_Comment.objects.get(comment_id=comment_id)
    
    if comment.voted_users.filter(username=request.user).exists():
        upvotes_downvotes_song_review_comment = comment.upvotes_downvotes_song_review_comment_set.get(username=request.user)
        if upvotes_downvotes_song_review_comment.vote_type == False:
            comment.downvotes -= 1
            comment.upvotes += 1
            comment.save()
            
            upvotes_downvotes_song_review_comment.vote_type = True
            upvotes_downvotes_song_review_comment.save()
        else:
            comment.upvotes -= 1
            comment.save()
            upvotes_downvotes_song_review_comment.delete()
    else:
        comment.upvotes += 1
        comment.save()
        
        upvotes_downvotes_song_review_comment = Upvotes_Downvotes_Song_Review_Comment(
            username = request.user,
            comment_id = comment,
            vote_type = True
        )
        upvotes_downvotes_song_review_comment.save()
    
    prev = request.POST.get('prev', '/')
    return redirect(prev)


@login_required
def downvoteSongReviewComment(request, review_id, comment_id):
    review = Song_Review.objects.get(review_id=review_id)
    comment = Song_Review_Comment.objects.get(comment_id=comment_id)
    
    if comment.voted_users.filter(username=request.user).exists():
        upvotes_downvotes_song_review_comment = comment.upvotes_downvotes_song_review_comment_set.get(username=request.user)
        if upvotes_downvotes_song_review_comment.vote_type == True:
            comment.upvotes -= 1
            comment.downvotes += 1
            comment.save()
            
            upvotes_downvotes_song_review_comment.vote_type = False
            upvotes_downvotes_song_review_comment.save()
        else:
            comment.downvotes -= 1
            comment.save()
            upvotes_downvotes_song_review_comment.delete()
    else:
        comment.downvotes += 1
        comment.save()
        
        upvotes_downvotes_song_review_comment = Upvotes_Downvotes_Song_Review_Comment(
            username = request.user,
            comment_id = comment,
            vote_type = False
        )
        upvotes_downvotes_song_review_comment.save()
    
    prev = request.POST.get('prev', '/')
    return redirect(prev)


@login_required
def upvoteAlbumReviewComment(request, review_id, comment_id):
    review = Album_Review.objects.get(review_id=review_id)
    comment = Album_Review_Comment.objects.get(comment_id=comment_id)
    
    if comment.voted_users.filter(username=request.user).exists():
        upvotes_downvotes_album_review_comment = comment.upvotes_downvotes_album_review_comment_set.get(username=request.user)
        if upvotes_downvotes_album_review_comment.vote_type == False:
            comment.downvotes -= 1
            comment.upvotes += 1
            comment.save()
            
            upvotes_downvotes_album_review_comment.vote_type = True
            upvotes_downvotes_album_review_comment.save()
        else:
            comment.upvotes -= 1
            comment.save()
            upvotes_downvotes_album_review_comment.delete()
    else:
        comment.upvotes += 1
        comment.save()
        
        upvotes_downvotes_album_review_comment = Upvotes_Downvotes_Album_Review_Comment(
            username = request.user,
            comment_id = comment,
            vote_type = True
        )
        upvotes_downvotes_album_review_comment.save()
    
    prev = request.POST.get('prev', '/')
    return redirect(prev)


@login_required
def downvoteAlbumReviewComment(request, review_id, comment_id):
    review = Album_Review.objects.get(review_id=review_id)
    comment = Album_Review_Comment.objects.get(comment_id=comment_id)
    
    if comment.voted_users.filter(username=request.user).exists():
        upvotes_downvotes_album_review_comment = comment.upvotes_downvotes_album_review_comment_set.get(username=request.user)
        if upvotes_downvotes_album_review_comment.vote_type == True:
            comment.upvotes -= 1
            comment.downvotes += 1
            comment.save()
            
            upvotes_downvotes_album_review_comment.vote_type = False
            upvotes_downvotes_album_review_comment.save()
        else:
            comment.downvotes -= 1
            comment.save()
            upvotes_downvotes_album_review_comment.delete()
    else:
        comment.downvotes += 1
        comment.save()
        
        upvotes_downvotes_album_review_comment = Upvotes_Downvotes_Album_Review_Comment(
            username = request.user,
            comment_id = comment,
            vote_type = False
        )
        upvotes_downvotes_album_review_comment.save()
    
    prev = request.POST.get('prev', '/')
    return redirect(prev)


def register(request):
    form = RegisterForm(auto_id=True)
    
    if request.method == 'POST':
        form = RegisterForm(request.POST, auto_id=True)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.fname = form.cleaned_data.get('fname')
            user.profile.lname = form.cleaned_data.get('lname')
            user.profile.age = form.cleaned_data.get('age')
            user.profile.gender = form.cleaned_data.get('gender')
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('/')
    
    template = loader.get_template('register.html')
    context = {
        'form': form
    }
    return HttpResponse(template.render(context, request))