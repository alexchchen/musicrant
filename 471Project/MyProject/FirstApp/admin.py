from django.contrib import admin
from .models import *

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "fname", "lname", "date_joined")

class ArtistAdmin(admin.ModelAdmin):
    list_display = ("artist_id", "name", "age", "gender")
    
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("album_id", "artist_id", "name", "date_released")
    
class SongAdmin(admin.ModelAdmin):
    list_display = ("song_id", "artist_id", "name", "album_id", "date_released")
    
class SongRatingAdmin(admin.ModelAdmin):
    list_display = ("rating_id", "username", "song_id", "date_given")
    
admin.site.register(User, UserAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(Song_Rating, SongRatingAdmin)