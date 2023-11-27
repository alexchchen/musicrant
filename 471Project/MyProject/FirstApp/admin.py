from django.contrib import admin
from .models import *

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "fname", "lname", "date_joined")

class ArtistAdmin(admin.ModelAdmin):
    list_display = ("artist_id", "name", "age", "gender")
    
class ArtistGenreAdmin(admin.ModelAdmin):
    list_display = ("artist_id", "genre")
    
class ProducerAdmin(admin.ModelAdmin):
    list_display = ("producer_id", "name", "age", "gender")
    
class ProducerGenreAdmin(admin.ModelAdmin):
    list_display = ("producer_id", "genre")
    
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("album_id", "artist_id", "name", "date_released")
    
class AlbumGenreAdmin(admin.ModelAdmin):
    list_display = ("album_id", "genre")
    
class SongAdmin(admin.ModelAdmin):
    list_display = ("song_id", "artist_id", "name", "album_id", "date_released")
    
class SongGenreAdmin(admin.ModelAdmin):
    list_display = ("song_id", "genre")
    
class SongRatingAdmin(admin.ModelAdmin):
    list_display = ("rating_id", "username", "song_id", "date_given")
    
class AlbumRatingAdmin(admin.ModelAdmin):
    list_display = ("rating_id", "username", "album_id", "date_given")
    
class SongReviewAdmin(admin.ModelAdmin):
    list_display = ("review_id", "username", "song_id", "rating_id", "title", "date_posted")
    
class AlbumReviewAdmin(admin.ModelAdmin):
    list_display = ("review_id", "username", "album_id", "rating_id", "title", "date_posted")
    
class SongReviewCommentAdmin(admin.ModelAdmin):
    list_display = ("comment_id", "review_id", "username", "upvotes", "downvotes", "date_posted")
     
class AlbumReviewCommentAdmin(admin.ModelAdmin):
    list_display = ("comment_id", "review_id", "username", "upvotes", "downvotes", "date_posted")
    
admin.site.register(User, UserAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Artist_Genre, ArtistGenreAdmin)
admin.site.register(Producer, ProducerAdmin)
admin.site.register(Producer_Genre, ProducerGenreAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Album_Genre, AlbumGenreAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(Song_Genre, SongGenreAdmin)
admin.site.register(Song_Rating, SongRatingAdmin)
admin.site.register(Album_Rating, AlbumRatingAdmin)
admin.site.register(Song_Review, SongReviewAdmin)
admin.site.register(Album_Review, AlbumReviewAdmin)
admin.site.register(Song_Review_Comment, SongReviewCommentAdmin)
admin.site.register(Album_Review_Comment, AlbumReviewCommentAdmin)