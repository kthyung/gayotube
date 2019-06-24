import requests
from bs4 import BeautifulSoup
import os
import django
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gayotube.settings")
django.setup()

from video.models import GenreVideo, PopGenreVideo
from selenium import webdriver


def parse_and_append(page_index, genre_type):
    print('kth parse_and_append() page_index : ' + str(page_index) + ' , genre_type : ' + str(genre_type))

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
    driver.get('https://www.melon.com/genre/song_list.htm' +
               '?startIndex=' + str(page_index) + '&pageSize=50' + '&gnrCode=GN' + str(genre_type) + '&steadyYn=Y')
    html = driver.page_source  ## 페이지의 elements모두 가져오기
    soup = BeautifulSoup(html, 'html.parser')  ## BeautifulSoup사용하기

    titles = soup.find_all("div", {"class": "ellipsis rank01"})
    artists = soup.find_all("div", {"class": "ellipsis rank02"})

    title = []
    artist = []

    if len(titles) == 0:
        return

    for t in titles:
        if t.find('a') is None:
            if t.find('div', {'class': 'ellipsis'}) is None:
                title.append(t.find('span', {'class': 'checkEllipsis'}).text)
            else:
                title.append(t.find('div', {'class': 'ellipsis'}).text)
        else:
            title.append(t.find('a').text)

    for a in artists:
        if a.find('a') is None:
            if a.find('div', {'class': 'ellipsis'}) is None:
                artist.append(a.find('span', {'class': 'checkEllipsis'}).text)
            else:
                artist.append(a.find('div', {'class': 'ellipsis'}).text)
        else:
            artist.append(a.find('a').text)

    for i in range(len(title)):
        videos = PopGenreVideo.objects.filter(type=genre_type, title=title[i]).order_by('chart')
        if len(videos) == 0:
            parse_and_append2(genre_type, page_index+i, title[i], artist[i])
    parse_and_append(page_index+50, genre_type)


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

    PopGenreVideo(type=video_type, chart=chart, title=title, artist=artist, video_key=key).save()
    time.sleep(2)


# 이 명령어는 이 파일이 import가 아닌 python에서 직접 실행할 경우에만 아래 코드가 동작하도록 합니다.
if __name__=='__main__':
    genreType = {900, 1000, 1100, 1200, 1300, 1400}
    for genre in genreType:
        parse_and_append(1, genre)

