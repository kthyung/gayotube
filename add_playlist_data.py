import requests
from bs4 import BeautifulSoup
import os
import django
import time
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gayotube.settings")
django.setup()

from video.models import Video, GenreVideo, PopVideo, PopGenreVideo, ArtistVideo, PopArtistVideo
from selenium import webdriver


def parse_and_append():
    print('kth parse_and_append()')

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
    driver.get('https://www.melon.com/dj/themegenre/djthemegenre_list.htm')
    html = driver.page_source  ## 페이지의 elements모두 가져오기
    soup = BeautifulSoup(html, 'html.parser')  ## BeautifulSoup사용하기

    recommend = soup.find("div", {"class": "recommend_list"})

    tag_code = []

    if recommend is not None:
        a_thumbs = recommend.find_all("a", {"class": "image_typeAll"})
        for a in a_thumbs:
            if 'href' in a.attrs:
                tag_script = a.attrs['href']
                index = tag_script.find("goDjTagHub(")
                tag_script2 = tag_script[index + 12:-3]
                tag_code.append(tag_script2)

    for i in range(len(tag_code)):
        parse_and_append2(1, tag_code[i])

    driver.close()
    driver.quit()

def parse_and_append2(page_index, tag_num):
    print('kth parse_and_append2() page_index : ' + str(page_index) + ' , tag_num : ' + tag_num)

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
    driver.get('https://www.melon.com/dj/tag/djtaghub_list.htm' +
               '?tagSeq=' + tag_num + '#params%5BtagSeq%5D=' + tag_num +
               '&params%5BorderBy%5D=POP' + '&po=pageObj' + '&startIndex=' + page_index)
    html = driver.page_source  ## 페이지의 elements모두 가져오기
    soup = BeautifulSoup(html, 'html.parser')  ## BeautifulSoup사용하기

    contents = soup.find_all("a", {"class": "image_typeAll"})

    playlist_code = []

    for c in contents:
        if 'href' in c.attrs:
            tag_script = c.attrs['href']
            index = tag_script.find("goDjPlaylistDetail(")
            tag_script2 = tag_script[index + 32:-3]
            playlist_code.append(tag_script2)


    for i in range(len(playlist_code)):
        parse_and_append3(1, playlist_code[i])

    driver.close()
    driver.quit()

    parse_and_append(page_index + 50, tag_num)


def parse_and_append3(video_type, chart, title, artist):
    print('kth parse_and_append3() video_type : ' + str(video_type) + ' , chart : ' + str(chart)
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

    driver.close()
    driver.quit()
    time.sleep(2)


# 이 명령어는 이 파일이 import가 아닌 python에서 직접 실행할 경우에만 아래 코드가 동작하도록 합니다.
if __name__=='__main__':
    parse_and_append()
    sys.exit()
