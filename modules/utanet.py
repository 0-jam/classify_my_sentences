import time
import urllib

from beautifulscraper import BeautifulScraper
from tqdm import tqdm

scraper = BeautifulScraper()
domain = 'https://www.uta-net.com'
attributes = {
    # 歌手名
    'artist': '1',
    # 曲名
    'title': '2',
    # 作詞者名
    'lyricist': '3',
    # 作曲者名
    'composer': '8',
}
match_modes = {
    # 完全一致
    'exact': '4',
    # 部分一致
    'partial': '3',
}


def get_page(url):
    body = scraper.go(url)
    time.sleep(1.0)

    return body


def search_song_ids(query, attribute='lyricist', match_mode='exact'):
    # クエリが日本語だと正しく処理されないのでエンコード
    search_url = domain + '/search/?Aselect=' + attributes[attribute] + '&Keyword=' + urllib.parse.quote(query) + '&Bselect=' + match_modes[match_mode] + '&sort='
    print('曲リストを取得しています：', search_url)

    bodies = [get_page(search_url)]

    pages = bodies[0].select('#page_list')[0].find_all('a')
    if len(pages) > 0:
        page_urls = [urllib.parse.urlparse(page.get('href')) for page in pages]
        queries = [urllib.parse.parse_qs(page.query) for page in page_urls]
        last_page = page_urls[-1]
        last_page_num = max([int(query['pnum'][0]) for query in queries])
        lpq = queries[-1]
        print(last_page_num, 'ページ見つかりました')

        for pnum in tqdm(range(2, last_page_num + 1)):
            # ページ番号だけ変えて新しくURLを生成
            lpq['pnum'] = [str(pnum)]
            page = urllib.parse.ParseResult(
                last_page.scheme,
                last_page.netloc,
                last_page.path,
                last_page.params,
                urllib.parse.urlencode(lpq, True),
                ''
            )
            page_url = urllib.parse.urlunparse(page)

            bodies.append(get_page(page_url))
    else:
        print('1ページ見つかりました')

    song_ids = []
    for body in bodies:
        # 歌詞ページのURLを抽出
        for td in body.select('.td1'):
            song_ids.append(td.find_all('a')[0].get('href'))

    return song_ids


def extract_song(song_id):
    song_url = domain + song_id

    print('曲データを抽出しています：', song_url)

    body = get_page(song_url)
    title = body.select('.song-infoboard h2')[0].text
    # 歌詞内の改行を半角スラッシュ/に置換して抽出
    lyric = body.find(id='kashi_area').get_text('/')
    artist = body.select('[itemprop="recordedAs"]')[0].text.strip()
    lyricist = body.select('[itemprop="lyricist"]')[0].text
    composer = body.select('[itemprop="composer"]')[0].text

    return {
        song_id: {
            'title': title,
            'lyric': lyric,
            'artist': artist,
            'lyricist': lyricist,
            'composer': composer,
        }
    }
