# 歌ネットスクレイパー

[歌ネット](https://www.uta-net.com/)から曲情報を抽出

---

1. [環境](#環境)
1. [インストール](#インストール)
1. [utanet_scraper.py](#utanet_scraperpy)
    1. [cat_json.py](#cat_jsonpy)

---

## 環境

- Python 3.9.4
- macOS Big Sur 11.3
- Windows 10 Build 21354

## インストール

`$ pipenv install`

## utanet_scraper.py

曲 ID を1（引数 `starts_with` で変更可能）から順番に曲情報を保存していく
指定された ID が欠番ならそれを飛ばして次の ID を抽出しにいく
`Ctrl + C` で強制終了しないと止まらないので注意
抽出結果 JSON は以下の通り：

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

### cat_json.py

- 指定したディレクトリ内のJSONファイルを結合する

```bash
# 入力はディレクトリ名，出力はファイル名
$ python cat_json.py text/lyrics_json_dir lyrics_all.json
```
