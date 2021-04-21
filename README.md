# 歌ネットスクレイパー

[歌ネット](https://www.uta-net.com/)から曲情報を抽出

---

1. [環境](#環境)
1. [インストール](#インストール)
1. [utanet_scraper.py](#utanet_scraperpy)
    1. [json_extractor.py](#json_extractorpy)
    1. [sqlite_converter.py](#sqlite_converterpy)

---

## 環境

- Python 3.9.4
- macOS Big Sur 11.3
- Windows 10 Build 21354

## インストール

`$ pipenv install`

## utanet_scraper.py

`$ pipenv run python utanet_scraper.py`

- 曲 ID を1（引数 `starts_with` で変更可能）から順番に曲情報を保存していく
    - 指定された ID が欠番ならそれを飛ばして次の ID を抽出しにいく
- `Ctrl + C` で強制終了しないと止まらないので注意
- 抽出結果は JSON `songs/<曲 ID>.json` として保存される
    - 出力先ディレクトリに同名のファイルが存在する場合それを飛ばす
    - `songs/` の部分は引数 `--output_dir` で変更可能
- 抽出結果 JSON は以下の通り：

```json
{
    "/song/<曲 ID>": {
        "title": "曲名",
        "lyric": "歌詞",
        "artist": "歌手名",
        "lyricist": "作詞者名",
        "composer": "作曲者名",
    }
}
```

### json_extractor.py

`$ pipenv run python json_extractor.py songs lyrics.txt`

- [utanet_scraper.py](#utanet_scraperpy) で出力した JSON （ディレクトリ単位で指定）から属性（デフォルト：lyrics）を一つ選んで抽出
- 抽出された属性はテキストで保存される
    - 曲ごとに改行
- 指定できる属性：
    - 'id'
    - 'title'
    - 'artist'
    - 'lyricist'
    - 'composer'
    - 'lyric'

### sqlite_converter.py

`$ pipenv run python sqlite_converter.py songs utanet.db`

[utanet_scraper.py](#utanet_scraperpy) で出力した JSON （ディレクトリ単位で指定）を SQLite3 データベースに変換して出力

テーブル名は `utanet_songs` で，カラムは以下の通り

```
song_id: 曲 ID （JSON ファイル名から抽出）
title: 曲名
lyric: 歌詞
artist: 歌手名
lyricist: 作詞者名
composer: 作曲者名
```
