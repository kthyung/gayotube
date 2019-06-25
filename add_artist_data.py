import requests
from bs4 import BeautifulSoup
import os
import django
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gayotube.settings")
django.setup()

from video.models import Video, GenreVideo, PopVideo, PopGenreVideo, ArtistVideo, PopArtistVideo
from selenium import webdriver


def parse_and_append(artist_name):
    print('kth parse_and_append() artist_name : ' + artist_name)

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/61.0.3163.100 Safari/537.36")
    options.add_argument("lang=ko_KR")  # 한국어!
    driver = webdriver.Chrome('/Users/kimtaehyeong/Desktop/python/gayotube/chromedriver', options=options)
    driver.implicitly_wait(3)
    driver.get('https://www.melon.com/search/song/index.htm' + '?startIndex=1' + '&pageSize=50' +
               '&q=' + artist_name + '&sort=hit' + '&section=artist' + '&subLinkOrText=L')
    html = driver.page_source  ## 페이지의 elements모두 가져오기
    soup = BeautifulSoup(html, 'html.parser')  ## BeautifulSoup사용하기

    titles = soup.find_all("a", {"class": "fc_gray"})

    title = []
    count = 0
    for t in titles:
        videos = PopArtistVideo.objects.filter(artist=artist_name.strip(), title=t.text.strip())
        if len(videos) == 0:
            title.append(t.text)
        count += 1
        if count >= 5:
            break

    for i in range(len(title)):
        parse_and_append2(10000, i+1, title[i], artist_name)


def parse_and_append2(video_type, chart, title, artist):
    print('kth parse_and_append2() video_type : ' + str(video_type) + ' , chart : ' + str(chart)
          + ' , title : ' + title + ' , artist : ' + artist)

    title2 = title.replace('&', ' N ', 1)
    artist2 = artist.replace('&', ' N ', 1)

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/61.0.3163.100 Safari/537.36")
    options.add_argument("lang=ko_KR")  # 한국어!
    driver = webdriver.Chrome('/Users/kimtaehyeong/Desktop/python/gayotube/chromedriver', options=options)
    driver.implicitly_wait(60)
    driver.get('https://www.youtube.com/results' +
               '?search_query=' + (artist2 + "+" + title2) + '&sp=EgIQAQ%253D%253D')
    html = driver.page_source  ## 페이지의 elements모두 가져오기
    soup = BeautifulSoup(html, 'html.parser')  ## BeautifulSoup사용하기

    key = ''
    links = soup.find_all("a", {"class": "yt-simple-endpoint style-scope ytd-video-renderer"})
    for l in links:
        if 'href' in l.attrs:
            youtube_text = l.attrs['href']
            index = youtube_text.find("watch?v=")
            youtube_text2 = youtube_text[index + 8:index + 26]
            if index != -1:
                key = youtube_text2.split('\"')[0]
        break
    PopArtistVideo(type=video_type, chart=chart, title=title.strip(), artist=artist.strip(), video_key=key).save()
    time.sleep(2)


# 이 명령어는 이 파일이 import가 아닌 python에서 직접 실행할 경우에만 아래 코드가 동작하도록 합니다.
if __name__=='__main__':
    # PopArtistVideo.objects.all().delete()
    #
    # artist_list1 = PopVideo.objects.all().order_by('artist', 'title')
    # artist_list2 = PopGenreVideo.objects.all().order_by('artist', 'title')
    #
    # for item in artist_list1:
    #     videos = PopArtistVideo.objects.filter(artist=item.artist.strip(), title=item.title.strip())
    #     if len(videos) == 0:
    #         PopArtistVideo(type=item.type, chart=item.chart, title=item.title.strip(),
    #                     artist=item.artist.strip(), video_key=item.video_key).save()
    #
    # for item2 in artist_list2:
    #     videos = PopArtistVideo.objects.filter(artist=item2.artist.strip(), title=item2.title.strip())
    #     if len(videos) == 0:
    #         PopArtistVideo(type=item2.type, chart=item2.chart, title=item2.title.strip(),
    #                     artist=item2.artist.strip(), video_key=item2.video_key).save()

    artists = PopArtistVideo.objects.all().order_by('artist').values_list('artist', flat=True).distinct()
    for artist in artists:
        if artist >= 'Peter Cetera':
            parse_and_append(artist)

