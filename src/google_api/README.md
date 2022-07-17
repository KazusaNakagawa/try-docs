## Gmail API

## 前提
- [Google Cloud](https://console.cloud.google.com/) で プロジェクト作成し、OAuth 2.0 クライアントの JSONファイルを用意
- Google Sheet 操作するために、[サービス アカウント キー](https://www.dragonarrow.work/articles/95) を作成
- [Gmail API](https://console.cloud.google.com/marketplace/product/google/gmail.googleapis.com) の有効化
- [Google Sheets API](https://console.cloud.google.com/marketplace/product/google/sheets.googleapis.com) の有効化

## 実行環境
- Python 3.9.1
- Mac M1

## 手順

1. 必要なファイル・環境変数を準備
  ```bash
  # ./token/credentials.json
  > OAuth 2.0 クライアントの JSONファイル
  
  # .env
  # 参照先: スプレッドシート名
  # >> https://docs.google.com/spreadsheets/d/{open_by_key}/edit#gid=0
  OPEN_BY_KEY={open_by_key}
  ```
2. package install
  ```bash
  pip install -r requirements.txt
  ```

3. `main.py` を実行する

4. メール送信されたか確認する


## 参考
- 
