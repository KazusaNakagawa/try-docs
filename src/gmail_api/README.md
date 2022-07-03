## Gmail API

## 前提
- Gmail API で プロジェクト作成し、OAuth 2.0 クライアントの JSONファイルを用意

## 実行環境
- Python 3.9.1
- Mac M1

## 操作

1. 必要なファイル・環境変数を準備
  ```bash
  # .token/credentials.json
  > OAuth 2.0 クライアントの JSONファイル
  
  # .env
  SENDER_ADDRESS=<送信者メールアドレス>
  TO_ADDRESS=<送信先メールアドレス>
  ```
2. `gmail_api.py` を実行する

3. メール送信されたか確認する


## 参考
- 