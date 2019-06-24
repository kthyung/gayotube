from django.contrib import admin
from .models import Video, PopVideo, ArtistVideo, PopArtistVideo, GenreVideo, PopGenreVideo

admin.site.register(Video)
admin.site.register(PopVideo)
admin.site.register(GenreVideo)
admin.site.register(PopGenreVideo)
admin.site.register(ArtistVideo)
admin.site.register(PopArtistVideo)

