from django.contrib import admin
from .models import *

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "fname", "lname", "date_joined")

class ArtistAdmin(admin.ModelAdmin):
    list_display = ("artist_id", "name", "age", "gender")
    
class ProducerAdmin(admin.ModelAdmin):
    list_display = ("producer_id", "name", "age", "gender")
    
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("album_id", "artist_id", "name", "date_released")
    
class SongAdmin(admin.ModelAdmin):
    list_display = ("song_id", "artist_id", "name", "album_id", "date_released")
    
class SongRatingAdmin(admin.ModelAdmin):
    list_display = ("rating_id", "username", "song_id", "date_given")
    
class AlbumRatingAdmin(admin.ModelAdmin):
    list_display = ("rating_id", "username", "album_id", "date_given")
    
class SongReviewAdmin(admin.ModelAdmin):
    list_display = ("review_id", "username", "song_id", "rating_id", "title", "date_posted")
    
class AlbumReviewAdmin(admin.ModelAdmin):
    list_display = ("review_id", "username", "album_id", "rating_id", "title", "date_posted")
    
admin.site.register(User, UserAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Producer, ProducerAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(Song_Rating, SongRatingAdmin)
admin.site.register(Album_Rating, AlbumRatingAdmin)
admin.site.register(Song_Review, SongReviewAdmin)
admin.site.register(Album_Review, AlbumReviewAdmin)