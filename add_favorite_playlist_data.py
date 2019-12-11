import requests
from bs4 import BeautifulSoup
import os
import django
import time
import sys
import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gayotube.settings")
django.setup()

from video.models import FavoritePlaylistVideo
from selenium import webdriver


def parse_and_append(page_index, playlist_num):
    print('kth parse_and_append() page_index : ' + str(page_index) + ' , playlist_num : ' + playlist_num)

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/61.0.3163.100 Safari/537.36")
    options.add_argument("lang=ko_KR")  # 한국어!
    driver = webdriver.Chrome('/Users/kim/Desktop/python/gayotube/chromedriver', options=options)
    driver.get('https://www.melon.com/mymusic/dj/mymusicdjplaylistview_inform.htm' +
               '?plylstSeq=' + playlist_num + '#params%5BplylstSeq%5D=' + playlist_num +
               '&po=pageObj' + '&startIndex=' + str(page_index))
    driver.implicitly_wait(2)
    html = driver.page_source  ## 페이지의 elements모두 가져오기
    soup = BeautifulSoup(html, 'html.parser')  ## BeautifulSoup사용하기

    name = soup.find("div", {"class": "ellipsis song_name"})
    name_txt = ''
    if name is not None:
        name_txt = name.text.strip()

    last_date = soup.find("span", {"class": "wrap_info entry meta date"})
    last_date_txt = ''
    if last_date is not None:
        last_date_txt = last_date.text.strip()

    #compare_date(last_date_txt)

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
        videos = FavoritePlaylistVideo.objects.filter(playlist_code=playlist_num, title=title[i]).order_by('title')
        if len(videos) == 0:
            parse_and_append2(playlist_num, name_txt, page_index + i, title[i], artist[i])

    driver.close()
    driver.quit()
    time.sleep(1)

    parse_and_append(page_index + 50, playlist_num)


def parse_and_append2(playlist_num, playlist_name, chart, title, artist):
    print('kth parse_and_append2() playlist_num : ' + playlist_num
          + ' , playlist_name : ' + playlist_name + ' , chart : ' + str(chart)
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
    driver = webdriver.Chrome('/Users/kim/Desktop/python/gayotube/chromedriver', options=options)
    driver.get('https://www.youtube.com/results' +
               '?search_query=' + (artist2 + "+" + title2) + '&sp=EgIQAQ%253D%253D')
    driver.implicitly_wait(2)
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

    FavoritePlaylistVideo(playlist_code=playlist_num, playlist_name=playlist_name,
                        type=30000, chart=chart, title=title, artist=artist, video_key=key).save()

    driver.close()
    driver.quit()
    time.sleep(1)


def compare_date(last_date_txt):
    print('kth dompare_date() last_date_txt : ' + last_date_txt)
    return True


# 이 명령어는 이 파일이 import가 아닌 python에서 직접 실행할 경우에만 아래 코드가 동작하도록 합니다.
if __name__=='__main__':
    #playlist_codes = ['408448859', '439421521', '405024652', '430995376']
    #playlist_codes = ['438600317', '428205764']
    playlist_codes = ['425182189', '438219771']

    FavoritePlaylistVideo.objects.all().delete()
    #FavoritePlaylistVideo.objects.exclude(playlist_code__in=playlist_codes).delete()

    #for code in playlist_codes:
    #    parse_and_append(1, code)
    #sys.exit()
