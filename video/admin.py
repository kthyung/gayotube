from django.contrib import admin
from .models import Video, PopVideo, ArtistVideo, PopArtistVideo
from .models import GenreVideo, PopGenreVideo, PlaylistVideo, FavoritePlaylistVideo

admin.site.register(Video)
admin.site.register(PopVideo)
admin.site.register(GenreVideo)
admin.site.register(PopGenreVideo)
admin.site.register(ArtistVideo)
admin.site.register(PopArtistVideo)
admin.site.register(PlaylistVideo)
admin.site.register(FavoritePlaylistVideo)

