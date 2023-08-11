import csv

# JSONデータの定義
data_json = [
    {
        "code": "bxxx",
        "url": "http://exsample/1663455145/666",
        "original": " 毎朝の連投のせいで、...",
        "posted_at": "2023/08/09 22:02:40",
        "media_type": "test_media"
    },
    {
        "code": "bxxx",
        "url": "http://exsample/1663455145/663",
        "original": " ＞ ：元信者 ：03/07/1xxxx------",
        "posted_at": "2023/08/08 20:37:57",
        "media_type": "test_media"
    },
    {
        "code": "bxxx",
        "url": "http://exsample/1663455145/662",
        "original": " ：元信者 ：03/07/------",
        "posted_at": "2023/08/09 21:37:57",
        "media_type": "test_media"
    },
    {
        "code": "bxxx",
        "url": "http://exsample/1663455145/661",
        "original": " 元信者 ：03/07/------",
        "posted_at": "2022/07/09 21:37:57",
        "media_type": "test_media"
    }
]

tsv_ = "./_data/data_output.tsv"

def json2tsv(data_json):
    """ JSONデータをTSVファイルに変換 """
    with open(tsv_, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data_json[0].keys(), delimiter='\t')
        writer.writeheader()
        for row in data_json:
            writer.writerow(row)

def tsv2json(tsv_):
    """ TSVファイルから posted_at の最小値・最大値を取得

    """
    with open(tsv_, 'r', newline='') as file:
        reader = csv.DictReader(file, delimiter='\t')
        # TSV ファイルの中身を確認

        posted_at = []
        rows = []

        for idx, row in enumerate(reader):
            if idx == 0:
                pass
            else:
              posted_at.append(row['posted_at'])
              rows.append({'code': row['code'], 'posted_at': row['posted_at'], 'url': row['url']})

        print('-'*20)

        # posted_at の最小値・最大値を取得. request_ できるように posted_at を変換
        min_ = min(posted_at).replace('/', '-').replace(' ', 'T')
        max_ = max(posted_at).replace('/', '-').replace(' ', 'T')
        # コードを取得
        code = data_json[0]['code']

    request_ = f"http://exsample?code={code}&bigin={min_}&end={max_}"

    return request_, rows

def match_data_json(data_json, rows):
    """ data_json と rows の posted_at を比較して、同じ posted_at のものを抽出 """
    match_data_json_ = []

    for row in rows:
        for d in data_json:
            if d['posted_at'] == row['posted_at'] and d['url'] == row['url']:
                match_data_json_.append(row)


    print('*'*20)
    print({'match': match_data_json_})
    print({'match': len(match_data_json_)})
    print('>'*20)

    return match_data_json_


target_data_json = [
    {
        "code": "bxxx",
        "url": "http://exsample/1663455145/666",
        "posted_at": "2023/08/09 22:02:40",
    },
    {
        "code": "bxxx",
        "url": "http://exsample/1663455145/663",
        "posted_at": "2023/08/08 20:37:57",
    },
    {
        "code": "bxxx",
        "url": "http://exsample/1663455145/662",
        "posted_at": "2023/08/09 21:37:57",
    },
    {
        "code": "bxxx",
        "url": "http://exsample/1663455145/662",
        "posted_at": "2022/07/09 21:37:57",
    },
    {
        "code": "bxxx",
        "url": "http://exsample/1663455145/669",
        "posted_at": "2023/04/09 21:37:57",
    },
]

def diff_data_json(target_data_json, match_data_json_):
    """ target_data_json と match_data_json_ を比較して 一致しないものを抽出 """
    diff_data_json = []

    for row in target_data_json:
        if row not in match_data_json_:
            diff_data_json.append(row)

    print({'diff_data_json': diff_data_json})
    print({'diff_data_json': len(diff_data_json)})


if __name__ == '__main__':
    """ TSVファイルに保存したデータを読み込み、target_data_json と比較する処理を想定
    $ python src/tools/search_data.py
    --------------------
    ********************
    {
        'match': [
            {'code': 'bxxx', 'posted_at': '2023/08/08 20:37:57', 'url': 'http://exsample/1663455145/663'},
            {'code': 'bxxx', 'posted_at': '2023/08/09 21:37:57', 'url': 'http://exsample/1663455145/662'},
            {'code': 'bxxx', 'posted_at': '2022/07/09 21:37:57', 'url': 'http://exsample/1663455145/661'}
        ]
    }
    {'match': 3}
    >>>>>>>>>>>>>>>>>>>>
    {
        'diff_data_json': [
            {'code': 'bxxx', 'url': 'http://exsample/1663455145/666', 'posted_at': '2023/08/09 22:02:40'},
            {'code': 'bxxx', 'url': 'http://exsample/1663455145/662', 'posted_at': '2022/07/09 21:37:57'},
            {'code': 'bxxx', 'url': 'http://exsample/1663455145/669', 'posted_at': '2023/04/09 21:37:57'}
        ]
    }
    {'diff_data_json': 3}

    """
    json2tsv(data_json)
    _, rows = tsv2json(tsv_)
    match_data_json_ = match_data_json(data_json, rows)
    diff_data_json(target_data_json, match_data_json_)
