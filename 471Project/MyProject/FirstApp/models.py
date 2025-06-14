from django.db import models
from django.db.models import CheckConstraint, Q, F
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

# Create your models here.

class Genre(models.TextChoices):
    POP = "POP", _("Pop")
    ROCK = "ROCK", _("Rock")
    HIPHOP = "HIPHOP", _("Hip Hop")
    RNB = "RNB", _("R&B")
    JAZZ = "JAZZ", _("Jazz")
    CLASSICAL = "CLASSICAL", _("Classical")
    FOLK = "FOLK", _("Folk")
    PUNK = "PUNK", _("Punk")
    METAL = "METAL", _("Metal")
    ELECTRONIC = "ELECTRONIC", _("Electronic")
    COUNTRY = "COUNTRY", _("Country")
    SOUL = "SOUL", _("Soul")
    FUNK = "FUNK", _("Funk")
    ACOUSTIC = "ACOUSTIC", _("Acoustic")
    DUBSTEP = "DUBSTEP", _("Dubstep")
    TRAP = "TRAP", _("Trap")
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    fname = models.CharField(max_length=15)
    lname = models.CharField(max_length=15)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=15, blank=True)
        
    class Meta:
        constraints = [
            CheckConstraint(
                check = Q(age__gt=0) & Q(age__lte=120),
                name = 'check_user_age'
            ),
        ]
        
    def __str__(self):
        return self.user.username
       
        
class Artist(models.Model):
    artist_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    bio = models.TextField()
    albums_produced = models.ManyToManyField('Album', through='Produces_Their_Album', related_name="artist_producers")
    singles_produced = models.ManyToManyField('Song', through='Produces_Their_Single', related_name="artist_producers")
        
    def __str__(self):
        return str(self.artist_id)
        

class Artist_Genre(models.Model):
    artist_id = models.ForeignKey('Artist', on_delete=models.CASCADE, related_name='genres')
    genre = models.CharField(max_length=50, choices=Genre.choices)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['artist_id', 'genre'], name='artist_genre_primary_key'
            )
        ]
    

class Producer(models.Model):
    producer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    bio = models.TextField(blank=True)
    albums_produced = models.ManyToManyField('Album', through='Produces_Album', related_name="producers")
    singles_produced = models.ManyToManyField('Song', through='Produces_Single', related_name="producers")
    
    def __str__(self):
        return str(self.producer_id)
        

class Producer_Genre(models.Model):
    producer_id = models.ForeignKey('Producer', on_delete=models.CASCADE, related_name='genres')
    genre = models.CharField(max_length=50, choices=Genre.choices)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['producer_id', 'genre'], name='producer_genre_primary_key'
            )
        ]
        
        
class Album(models.Model):
    album_id = models.AutoField(primary_key=True)
    artist_id = models.ForeignKey('Artist', on_delete=models.CASCADE, related_name='albums')
    name = models.CharField(max_length=128)
    date_released = models.DateField()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['album_id', 'artist_id'], name='album_primary_key'
            )
        ]
        
    def __str__(self):
        return str(self.album_id)
        
        
class Album_Genre(models.Model):
    album_id = models.ForeignKey('Album', on_delete=models.CASCADE, related_name='genres')
    genre = models.CharField(max_length=50, choices=Genre.choices)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['album_id', 'genre'], name='album_genre_primary_key'
            )
        ]


class Song(models.Model):
    song_id = models.AutoField(primary_key=True)
    artist_id = models.ForeignKey('Artist', on_delete=models.CASCADE, related_name='songs')
    album_id = models.ForeignKey('Album', null=True, blank=True, on_delete=models.SET_NULL, related_name='songs')
    name = models.CharField(max_length=128)
    date_released = models.DateField()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['song_id', 'artist_id'], name='song_primary_key'
            )
        ]
        
    def __str__(self):
        return str(self.song_id)
        
        
class Song_Genre(models.Model):
    song_id = models.ForeignKey('Song', on_delete=models.CASCADE, related_name='genres')
    genre = models.CharField(max_length=50, choices=Genre.choices)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['song_id', 'genre'], name='song_genre_primary_key'
            )
        ]
        
        
class Song_Rating(models.Model):
    rating_id = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='song_ratings')
    song_id = models.ForeignKey('Song', on_delete=models.CASCADE, related_name='ratings')
    originality_score = models.IntegerField()
    lyric_score = models.IntegerField()
    vibe_score = models.IntegerField()
    instrumental_score = models.IntegerField()
    date_given = models.DateField(auto_now_add=True)
    
    class Meta:
        constraints = [
            CheckConstraint(
                check = Q(originality_score__gte=0) & Q(originality_score__lte=10),
                name = 'check_song_rating_originality_score'
            ),
            CheckConstraint(
                check = Q(lyric_score__gte=0) & Q(lyric_score__lte=10),
                name = 'check_song_rating_lyric_score'
            ),
            CheckConstraint(
                check = Q(vibe_score__gte=0) & Q(vibe_score__lte=10),
                name = 'check_song_rating_vibe_score'
            ),
            CheckConstraint(
                check = Q(instrumental_score__gte=0) & Q(instrumental_score__lte=10),
                name = 'check_song_rating_instrumental_score'
            ),
            models.UniqueConstraint(
                fields=['song_id', 'username'], name='song_rating_primary_key'
            )
        ]
    
    def __str__(self):
        return str(self.rating_id)
        

class Album_Rating(models.Model):
    rating_id = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='album_ratings')
    album_id = models.ForeignKey('Album', on_delete=models.CASCADE, related_name='ratings')
    originality_score = models.IntegerField()
    lyric_score = models.IntegerField()
    vibe_score = models.IntegerField()
    instrumental_score = models.IntegerField()
    album_flow_score = models.IntegerField()
    date_given = models.DateField(auto_now_add=True)
    
    class Meta:
        constraints = [
            CheckConstraint(
                check = Q(originality_score__gte=0) & Q(originality_score__lte=10),
                name = 'check_album_rating_originality_score'
            ),
            CheckConstraint(
                check = Q(lyric_score__gte=0) & Q(lyric_score__lte=10),
                name = 'check_album_rating_lyric_score'
            ),
            CheckConstraint(
                check = Q(vibe_score__gte=0) & Q(vibe_score__lte=10),
                name = 'check_album_rating_vibe_score'
            ),
            CheckConstraint(
                check = Q(instrumental_score__gte=0) & Q(instrumental_score__lte=10),
                name = 'check_album_rating_instrumental_score'
            ),
            CheckConstraint(
                check = Q(album_flow_score__gte=0) & Q(album_flow_score__lte=10),
                name = 'check_album_rating_album_flow_score'
            ),
            models.UniqueConstraint(
                fields=['album_id', 'username'], name='album_rating_primary_key'
            )
        ]
    
    def __str__(self):
        return str(self.rating_id)


class Song_Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='song_reviews_posted')
    song_id = models.ForeignKey('Song', on_delete=models.CASCADE, related_name='reviews')
    rating_id = models.ForeignKey('Song_Rating', on_delete=models.CASCADE, related_name='review')
    title = models.CharField(max_length=50)
    body = models.TextField()
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    date_posted = models.DateField(auto_now_add=True)
    voted_users = models.ManyToManyField(User, through='Upvotes_Downvotes_Song_Review', related_name='song_reviews_voted')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['song_id', 'username'], name='song_review_primary_key'
            )
        ]
        
    def __str__(self):
        return str(self.review_id)


class Album_Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='album_reviews_posted')
    album_id = models.ForeignKey('Album', on_delete=models.CASCADE, related_name='reviews')
    rating_id = models.ForeignKey('Album_Rating', on_delete=models.CASCADE, related_name='review')
    title = models.CharField(max_length=50)
    body = models.TextField()
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    date_posted = models.DateField(auto_now_add=True)
    voted_users = models.ManyToManyField(User, through='Upvotes_Downvotes_Album_Review', related_name='album_reviews_voted')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['album_id', 'username'], name='album_review_primary_key'
            )
        ]

    def __str__(self):
        return str(self.review_id)
        
        
class Song_Review_Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    review_id = models.ForeignKey('Song_Review', on_delete=models.CASCADE, related_name='comments')
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='song_review_comments_posted')
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    body = models.TextField()
    date_posted = models.DateField(auto_now_add=True)
    voted_users = models.ManyToManyField(User, through='Upvotes_Downvotes_Song_Review_Comment', related_name='song_review_comments_voted')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['comment_id', 'review_id'], name='song_review_comment_primary_key'
            )
        ]
        
    def __str__(self):
        return str(self.comment_id)
        
        
class Album_Review_Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    review_id = models.ForeignKey('Album_Review', on_delete=models.CASCADE, related_name='comments')
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='album_review_comments_posted')
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    body = models.TextField()
    date_posted = models.DateField(auto_now_add=True)
    voted_users = models.ManyToManyField(User, through='Upvotes_Downvotes_Album_Review_Comment', related_name='album_review_comments_voted')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['comment_id', 'review_id'], name='album_review_comment_primary_key'
            )
        ]
        
    def __str__(self):
        return str(self.comment_id)
        
        
class Upvotes_Downvotes_Song_Review(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    review_id = models.ForeignKey('Song_Review', on_delete=models.CASCADE)
    vote_type = models.BooleanField()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'review_id'], name='upvotes_downvotes_song_review_primary_key'
            )
        ]
        
        
class Upvotes_Downvotes_Album_Review(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    review_id = models.ForeignKey('Album_Review', on_delete=models.CASCADE)
    vote_type = models.BooleanField()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'review_id'], name='upvotes_downvotes_album_review_primary_key'
            )
        ]
        

class Upvotes_Downvotes_Song_Review_Comment(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_id = models.ForeignKey('Song_Review_Comment', on_delete=models.CASCADE)
    vote_type = models.BooleanField()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'comment_id'], name='upvotes_downvotes_song_review_comment_primary_key'
            )
        ]
        

class Upvotes_Downvotes_Album_Review_Comment(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_id = models.ForeignKey('Album_Review_Comment', on_delete=models.CASCADE)
    vote_type = models.BooleanField()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'comment_id'], name='upvotes_downvotes_album_review_comment_primary_key'
            )
        ]
        

class Produces_Album(models.Model):
    producer_id = models.ForeignKey('Producer', on_delete=models.CASCADE)
    album_id = models.ForeignKey('Album', on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['producer_id', 'album_id'], name='produces_album_primary_key'
            )
        ]
        
        
class Produces_Single(models.Model):
    producer_id = models.ForeignKey('Producer', on_delete=models.CASCADE)
    song_id = models.ForeignKey('Song', on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['producer_id', 'song_id'], name='produces_single_primary_key'
            )
        ]
        

class Produces_Their_Album(models.Model):
    artist_id = models.ForeignKey('Artist', on_delete=models.CASCADE)
    album_id = models.ForeignKey('Album', on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['artist_id', 'album_id'], name='produces_their_album_primary_key'
            )
        ]
        
        
class Produces_Their_Single(models.Model):
    artist_id = models.ForeignKey('Artist', on_delete=models.CASCADE)
    song_id = models.ForeignKey('Song', on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['artist_id', 'song_id'], name='produces_their_single_primary_key'
            )
        ]