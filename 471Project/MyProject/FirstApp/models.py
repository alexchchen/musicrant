from django.db import models
from django.db.models import CheckConstraint, Q, F

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=15, primary_key=True)
    fname = models.CharField(max_length=15)
    lname = models.CharField(max_length=15)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=15, blank=True)
    password = models.CharField(max_length=15)
    admin_flag = models.BooleanField(default=False)
    client_flag = models.BooleanField(default=True)
    date_joined = models.DateField(auto_now_add=True)
    
    class Meta:
        constraints = [
            CheckConstraint(
                check = Q(age__gt=0) & Q(age__lte=120),
                name = 'check_user_age'
            ),
        ]
       
        
class Artist(models.Model):
    artist_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=15, blank=True)
    bio = models.TextField(blank=True)
    
    class Meta:
        constraints = [
            CheckConstraint(
                check = Q(age__gt=0) & Q(age__lte=120),
                name = 'check_artist_age'
            )
        ]
        

class Producer(models.Model):
    producer_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=15, blank=True)
    bio = models.TextField(blank=True)
    
    class Meta:
        constraints = [
            CheckConstraint(
                check = Q(age__gt=0) & Q(age__lte=120),
                name = 'check_producer_age'
            )
        ]
        
        
class Album(models.Model):
    album_id = models.IntegerField(primary_key=True)
    artist_id = models.ForeignKey('Artist', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    date_released = models.DateField()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['album_id', 'artist_id'], name='album_primary_key'
            )
        ]


class Song(models.Model):
    song_id = models.IntegerField(primary_key=True)
    artist_id = models.ForeignKey('Artist', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    album_id = models.ForeignKey('Album', null=True, blank=True, on_delete=models.SET_NULL)
    date_released = models.DateField()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['song_id', 'artist_id'], name='song_primary_key'
            )
        ]
        
        
class Song_Rating(models.Model):
    rating_id = models.IntegerField(primary_key=True)
    originality_score = models.IntegerField()
    lyric_score = models.IntegerField()
    vibe_score = models.IntegerField()
    instrumental_score = models.IntegerField()
    username = models.ForeignKey('User', on_delete=models.CASCADE)
    song_id = models.ForeignKey('Song', on_delete=models.CASCADE)
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
        ]
        
