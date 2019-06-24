from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Video, PopVideo, ArtistVideo, PopArtistVideo, GenreVideo, PopGenreVideo


def video_blank(request):
    return redirect('/index/2018')


def video_index(request, year):
    videos = Video.objects.filter(type=year).order_by('chart')
    return render(request, 'video/index.html',
                  {'view_type': 'kpop', 'videos': videos, 'video_year': year, 'video_index': 1})


def video_pop_index(request, year):
    videos = PopVideo.objects.filter(type=year).order_by('chart')
    return render(request, 'video/index.html',
                  {'view_type': 'pop', 'videos': videos, 'video_year': year, 'video_index': 1})


def video_genre(request, type):
    videos = GenreVideo.objects.filter(type=type).order_by('chart')
    return render(request, 'video/index.html',
                  {'view_type': 'genre_kpop', 'videos': videos, 'genre_type': type, 'video_index': 1})


def video_pop_genre(request, type):
    videos = PopGenreVideo.objects.filter(type=type).order_by('chart')
    return render(request, 'video/index.html',
                  {'view_type': 'genre_pop', 'videos': videos, 'genre_type': type, 'video_index': 1})


def video_search(request):
    result_list = []
    word = ''

    if request.method == 'POST':
        word = request.POST.get('search_text', '')
        search_type = request.POST.get('search_type', '')
        if search_type == 'kpop_artist':
            result_list = ArtistVideo.objects.filter(artist__contains=word).order_by('title')
        elif search_type == 'kpop_title':
            result_list = ArtistVideo.objects.filter(title__contains=word).order_by('title')
        elif search_type == 'pop_artist':
            result_list = PopArtistVideo.objects.filter(artist__contains=word).order_by('title')
        elif search_type == 'pop_title':
            result_list = PopArtistVideo.objects.filter(title__contains=word).order_by('title')

    return render(request, 'video/index.html',
                  {'view_type': search_type, 'videos': result_list, 'word': word, 'video_index': 1})


def video_artist(request, artist, index):
    first_artist = get_first_chosung(artist)
    artists = ArtistVideo.objects.filter(artist__range=(first_artist, first_artist)).ordeer_by('artist', 'chart')
    return render(request, 'video/artist.html',
                  {'view_type': 'pop', 'artists': artists, 'video_index': index})


def video_list(request):
    video_list = Video.objects.all()
    return render(request, 'video/video_list.html', {'video_list': video_list})


def video_new(request):
    if request.method == 'POST':
        title = request.POST['title']
        artist = request.POST['artist']
        video_key = request.POST['video_key']
        Video.objects.create(title=title, artist=artist, video_key=video_key)
        return redirect('/')
    elif request.method == 'GET':
        return render(request, 'video/video_new.html')


def video_detail(request, video_id):
    video = Video.objects.get(id=video_id)
    return render(request, 'video/video_detail.html', {'video': video})


def get_first_chosung(text):
    CHOSUNG_START_LETTER = 4352
    JAMO_START_LETTER = 44032
    JAMO_END_LETTER = 55203
    JAMO_CYCLE = 588

    def is_hangul(ch):
        return ord(ch) >= JAMO_START_LETTER and ord(ch) <= JAMO_END_LETTER

    first = text[0]
    if is_hangul(first):  # 한글이 아닌 글자는 걸러냅니다.
        result = chr(int((ord(first) - JAMO_START_LETTER) / JAMO_CYCLE + CHOSUNG_START_LETTER))
    else:
        result = first

    return result

