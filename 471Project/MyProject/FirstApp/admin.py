from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile
    max_num = 1
    can_delete = False
    
class UserAdmin(BaseUserAdmin):
    def add_view(self, *args, **kwargs):
        self.inlines = []
        return super(UserAdmin, self).add_view(*args, **kwargs)

    def change_view(self, *args, **kwargs):
        self.inlines = [ProfileInline]
        return super(UserAdmin, self).change_view(*args, **kwargs)
  
    list_display = ("username", "fname", "lname", "age", "gender")
    
    def fname(self, obj):
        return Profile.objects.get(user=obj).fname
    def lname(self, obj):
        return Profile.objects.get(user=obj).lname
    def age(self, obj):
        return Profile.objects.get(user=obj).age
    def gender(self, obj):
        return Profile.objects.get(user=obj).gender

class ArtistAdmin(admin.ModelAdmin):
    list_display = ("artist_id", "name")
    
class ArtistGenreAdmin(admin.ModelAdmin):
    list_display = ("artist_id", "genre")
    
class ProducerAdmin(admin.ModelAdmin):
    list_display = ("producer_id", "name")
    
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
    list_display = ("rating_id", "username", "song_id", "originality_score", "lyric_score", "vibe_score", "instrumental_score", "date_given")
    
class AlbumRatingAdmin(admin.ModelAdmin):
    list_display = ("rating_id", "username", "album_id", "originality_score", "lyric_score", "vibe_score", "instrumental_score", "album_flow_score", "date_given")
    
class SongReviewAdmin(admin.ModelAdmin):
    list_display = ("review_id", "username", "song_id", "rating_id", "title", "date_posted")
    
class AlbumReviewAdmin(admin.ModelAdmin):
    list_display = ("review_id", "username", "album_id", "rating_id", "title", "date_posted")
    
class SongReviewCommentAdmin(admin.ModelAdmin):
    list_display = ("comment_id", "review_id", "username", "upvotes", "downvotes", "date_posted")
     
class AlbumReviewCommentAdmin(admin.ModelAdmin):
    list_display = ("comment_id", "review_id", "username", "upvotes", "downvotes", "date_posted")

class UpvotesDownvotesSongReviewAdmin(admin.ModelAdmin):
    list_display = ("username", "review_id", "vote_type")

class UpvotesDownvotesAlbumReviewAdmin(admin.ModelAdmin):
    list_display = ("username", "review_id", "vote_type")

class UpvotesDownvotesSongReviewCommentAdmin(admin.ModelAdmin):
    list_display = ("username", "comment_id", "vote_type")
    
class UpvotesDownvotesAlbumReviewCommentAdmin(admin.ModelAdmin):
    list_display = ("username", "comment_id", "vote_type")
    
class ProducesAlbumAdmin(admin.ModelAdmin):
    list_display = ("producer_id", "album_id")
    
class ProducesSingleAdmin(admin.ModelAdmin):
    list_display = ("producer_id", "song_id")
    
class ProducesTheirAlbumAdmin(admin.ModelAdmin):
    list_display = ("artist_id", "album_id")
    
class ProducesTheirSingleAdmin(admin.ModelAdmin):
    list_display = ("artist_id", "song_id")
    
admin.site.unregister(User)
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
admin.site.register(Upvotes_Downvotes_Song_Review, UpvotesDownvotesSongReviewAdmin)
admin.site.register(Upvotes_Downvotes_Album_Review, UpvotesDownvotesAlbumReviewAdmin)
admin.site.register(Upvotes_Downvotes_Song_Review_Comment, UpvotesDownvotesSongReviewCommentAdmin)
admin.site.register(Upvotes_Downvotes_Album_Review_Comment, UpvotesDownvotesAlbumReviewCommentAdmin)
admin.site.register(Produces_Album, ProducesAlbumAdmin)
admin.site.register(Produces_Single, ProducesSingleAdmin)
admin.site.register(Produces_Their_Album, ProducesTheirAlbumAdmin)
admin.site.register(Produces_Their_Single, ProducesTheirSingleAdmin)