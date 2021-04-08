import argparse
import json
import time
import urllib
from pathlib import Path

from beautifulscraper import BeautifulScraper

scraper = BeautifulScraper()
domain = 'https://www.uta-net.com'


def get_page(url):
    body = scraper.go(url)
    time.sleep(1.0)

    return body


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


def main():
    parser = argparse.ArgumentParser(description='曲情報を抽出（Ctrl + C で中止）')
    parser.add_argument('-o', '--output_dir', type=str, default='songs', help="出力ディレクトリ名（デフォルト：'./songs'）")
    parser.add_argument('-s', '--starts_with', type=int, default=1, help="指定した ID から抽出を開始（デフォルト：'1'）")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    Path.mkdir(output_dir, parents=True, exist_ok=True)

    song_count = args.starts_with
    while True:
        try:
            song_dict = extract_song('/song/{}/'.format(song_count))

            with output_dir.joinpath('{}.json'.format(song_count)).open('w', encoding='utf-8') as song_json:
                song_json.write(json.dumps(song_dict, ensure_ascii=False, indent=2))
        except urllib.error.HTTPError:
            print('ID が見つかりません')

            continue
        finally:
            song_count += 1


if __name__ == '__main__':
    main()
