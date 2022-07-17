## Try Google API

## 前提
- [Google Cloud](https://console.cloud.google.com/) で プロジェクト作成し、OAuth 2.0 クライアントの JSONファイルを用意
- Google Sheet 操作するために、[サービス アカウント キー](https://www.dragonarrow.work/articles/95) を作成
- 参照したいスプレッドシートの設定
- [Gmail API](https://console.cloud.google.com/marketplace/product/google/gmail.googleapis.com) の有効化
- [Google Sheets API](https://console.cloud.google.com/marketplace/product/google/sheets.googleapis.com) の有効化

## 実行環境
- Python 3.9.1
- Mac M1

## 手順

1. 必要なファイル準備

|Path|Details|
|:-|:-|
|`./token/credentials.json`|OAuth 2.0 クライアントの JSONファイル|
|`gmail-api-355022-service-account-key.json`|サービスアカウントキー ※1|
※1: 任意のjson ファイル名でよい. [SheetApi](https://github.com/KazusaNakagawa/try-docs/blob/eca14a49fa233b79ee29568c83c6a36770957ce8/src/google_api/models/sheets_api.py#L15) でファイル名をハードコーティングしている

2. 環境設定値
  ```bash
  # .env
  # mail
  SENDER_ADDRESS={sender address}
  TO_ADDRESS={to address}

  # 参照先: スプレッドシート名
  # >> https://docs.google.com/spreadsheets/d/{open_by_key}/edit#gid=0
  OPEN_BY_KEY={open_by_key}
  ```
3. package install
  ```bash
  pip install -r requirements.txt
  ```

4. `main.py` を実行する

5. メール送信されたか確認する


## 参考
- 
