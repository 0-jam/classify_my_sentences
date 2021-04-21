import argparse
import json
import sqlite3
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description='utanet_scraper.py で抽出した JSON ファイルを SQLite DB に変換')
    parser.add_argument('json_dir', type=str, help='JSON ファイルのあるディレクトリ')
    parser.add_argument('sqlite_file', type=str, help='SQLite ファイル')
    args = parser.parse_args()

    sqlite_file = Path(args.sqlite_file)

    sqlite_connection = sqlite3.connect(sqlite_file)
    sqlite_cursor = sqlite_connection.cursor()

    sqlite_cursor.execute('''
        create table if not exists utanet_songs(
            song_id int primary key,
            title text,
            lyric text,
            artist text,
            lyricist text,
            composer text
        )
    ''')

    query_string = '''
        insert into utanet_songs(song_id, title, lyric, artist, lyricist, composer)
        values (?, ?, ?, ?, ?, ?)
    '''

    for json_path in Path(args.json_dir).iterdir():
        with json_path.open() as json_file:
            song_dict = json.load(json_file)

        print('処理中：', json_path.name)

        song_id = int(json_path.stem)
        song_data = tuple(song_dict.values())[0]

        query_values = (
            song_id,
            song_data['title'],
            song_data['lyric'],
            song_data['artist'],
            song_data['lyricist'],
            song_data['composer'],
        )

        sqlite_cursor.execute(query_string, query_values)
        sqlite_connection.commit()

    sqlite_connection.close()

    print('完了')


if __name__ == "__main__":
    main()
