import argparse
import json
import urllib
from pathlib import Path

from modules.utanet import extract_song


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
            song_json_path = output_dir.joinpath('{}.json'.format(song_count))

            if song_json_path.is_file():
                print('スキップ：ファイル "{}" は既に存在します'.format(song_json_path))

                continue

            song_dict = extract_song('/song/{}/'.format(song_count))

            with song_json_path.open('w', encoding='utf-8') as song_json:
                song_json.write(json.dumps(song_dict, ensure_ascii=False, indent=2))
        except urllib.error.HTTPError:
            print('ID: {} が見つかりません'.format(song_count))

            continue
        finally:
            song_count += 1


if __name__ == '__main__':
    main()
