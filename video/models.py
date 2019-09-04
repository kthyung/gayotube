from django.db import models


class Video(models.Model):
    type = models.PositiveIntegerField(default=0)
    chart = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200, default='')
    video_key = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class PopVideo(models.Model):
    type = models.PositiveIntegerField(default=0)
    chart = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200, default='')
    video_key = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class GenreVideo(models.Model):
    type = models.PositiveIntegerField(default=0)
    chart = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200, default='')
    video_key = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class PopGenreVideo(models.Model):
    type = models.PositiveIntegerField(default=0)
    chart = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200, default='')
    video_key = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class ArtistVideo(models.Model):
    type = models.PositiveIntegerField(default=0)
    chart = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200, default='')
    video_key = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class PopArtistVideo(models.Model):
    type = models.PositiveIntegerField(default=0)
    chart = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200, default='')
    video_key = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class PlaylistVideo(models.Model):
    tag_code = models.CharField(max_length=20)
    playlist_code = models.CharField(max_length=20)
    playlist_name = models.CharField(max_length=200)
    type = models.PositiveIntegerField(default=0)
    chart = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200, default='')
    video_key = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class FavoritePlaylistVideo(models.Model):
    playlist_code = models.CharField(max_length=20)
    playlist_name = models.CharField(max_length=200)
    type = models.PositiveIntegerField(default=0)
    chart = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200, default='')
    video_key = models.CharField(max_length=20)

    def __str__(self):
        return self.title