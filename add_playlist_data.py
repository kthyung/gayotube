import requests
from bs4 import BeautifulSoup
import os
import django
import time
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gayotube.settings")
django.setup()

from video.models import Video, GenreVideo, PopVideo, PopGenreVideo, ArtistVideo, PopArtistVideo, PlaylistVideo
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
    driver.get('https://www.melon.com/dj/themegenre/djthemegenre_list.htm')
    driver.implicitly_wait(2)
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
    time.sleep(1)


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
    driver.get('https://www.melon.com/dj/tag/djtaghub_list.htm' +
               '?tagSeq=' + tag_num + '#params%5BtagSeq%5D=' + tag_num +
               '&params%5BorderBy%5D=POP' + '&po=pageObj' + '&startIndex=' + str(page_index))
    driver.implicitly_wait(2)
    html = driver.page_source  ## 페이지의 elements모두 가져오기
    soup = BeautifulSoup(html, 'html.parser')  ## BeautifulSoup사용하기

    contents = soup.find_all("a", {"class": "image_typeAll"})
    likes = soup.find_all("button", {"class": "button_etc like btn_djplylst_like"})

    playlist_code = []

    if len(contents) == 0:
        return

    for i, c in enumerate(contents):
        if 'href' in c.attrs:
            tag_script = c.attrs['href']
            index = tag_script.find("goDjPlaylistDetail(")
            tag_script2 = tag_script[index + 32:-3]

            cnt = likes[i].find("span", {"class": "cnt"})
            if cnt is not None:
                cnt_text = cnt.text.replace(" ", "").replace(",", "")
                index2 = cnt_text.find("총건수")
                cnt_text2 = cnt_text[index2 + 3:]
                try:
                    if int(cnt_text2) >= 2000:
                        playlist_code.append(tag_script2)
                except Exception as ex:
                    print('kth error : ', ex)
                    break

    for i in range(len(playlist_code)):
        #videos = PlaylistVideo.objects.filter(playlist_code=playlist_code[i]).order_by('playlist_code')
        #if len(videos) == 0:
        parse_and_append3(1, tag_num, playlist_code[i])

    driver.close()
    driver.quit()
    time.sleep(1)

    parse_and_append2(page_index + 20, tag_num)


def parse_and_append3(page_index, tag_num, playlist_num):
    print('kth parse_and_append3() page_index : ' + str(page_index) +
          ' , tag_num : ' + tag_num + ' , playlist_num : ' + playlist_num)

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/61.0.3163.100 Safari/537.36")
    options.add_argument("lang=ko_KR")  # 한국어!
    driver = webdriver.Chrome('/Users/kimtaehyeong/Desktop/python/gayotube/chromedriver', options=options)
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
        videos = PlaylistVideo.objects.filter(playlist_code=playlist_num, title=title[i]).order_by('title')
        if len(videos) == 0:
            parse_and_append4(20000, tag_num, playlist_num, name_txt, page_index + i, title[i], artist[i])

    driver.close()
    driver.quit()
    time.sleep(1)

    parse_and_append3(page_index + 50, tag_num, playlist_num)


def parse_and_append4(video_type, tag_num, playlist_num, playlist_name, chart, title, artist):
    print('kth parse_and_append4() video_type : ' + str(video_type)
          + ' , tag_num : ' + tag_num + ' , playlist_num : ' + playlist_num
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
    driver = webdriver.Chrome('/Users/kimtaehyeong/Desktop/python/gayotube/chromedriver', options=options)
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

    PlaylistVideo(tag_code=tag_num, playlist_code=playlist_num, playlist_name=playlist_name,
                  type=video_type, chart=chart, title=title, artist=artist, video_key=key).save()

    driver.close()
    driver.quit()
    time.sleep(1)


# 이 명령어는 이 파일이 import가 아닌 python에서 직접 실행할 경우에만 아래 코드가 동작하도록 합니다.
if __name__=='__main__':
    parse_and_append()
    sys.exit()
