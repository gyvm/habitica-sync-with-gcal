# habitica-task-sync-with-gcal
habitica-task-sync-with-gcalはhabiticaでタスク（習慣、日課、To Do）を完了した際に、Googleカレンダーにイベントを登録するためのスクリプトです。  
Google Cloud Runで動作します。起動方法は以下をご確認ください。　

<img width="405" alt="スクリーンショット 2021-08-30 5 46 00" src="https://user-images.githubusercontent.com/77700130/131265506-8178fda9-d18d-4a7a-806a-9449e349f139.png">

## 起動方法
### 手順
1. Google Calendar APIを有効化
1. GCPのサービスアカウントを作成
1. Googleカレンダーへサービスアカウントを登録
1. `main.py`の編集
1. デプロイ

### 必要な情報
- Habitica User ID
- Habitica API Token
    - Habitica関連の情報はHabiticaの設定ページから確認可能
    - https://habitica.com/user/settings/api
- GoogleカレンダーID

## 1. Google Calendar APIを有効化する
1. https://console.cloud.google.com/apis/library からGoogle Calendar APIを検索し有効化する
    - 参考
      - https://developers.google.com/workspace/guides/create-project#enable-api
<img width="551" alt="スクリーンショット 2021-08-30 4 25 09" src="https://user-images.githubusercontent.com/77700130/131264596-5b0973d9-b7eb-4396-81d4-e3594494af1c.png">

## 2. GCPのサービスアカウントを作成する

1. GCPコンソール「IAMと管理」の「サービスアカウント」ページにて「サービスアカウントを作成」を行う
    - https://console.cloud.google.com/iam-admin/serviceaccounts
    - 任意の「サービスアカウント名」を入力する(その他の箇所は未入力でも良い)
<img width="836" alt="スクリーンショット 2021-08-30 5 30 10" src="https://user-images.githubusercontent.com/77700130/131264611-7347b748-7663-4560-aae9-5988c9ebd61d.png">

2. サービスアカウントの鍵を作成する
    - 作成された対象の縦三点リーダー(メニュー)より「鍵を管理」を選択する
    - 「新しい鍵を作成」にてJSON型の秘密鍵を生成、ダウンロードする
<img width="1027" alt="スクリーンショット 2021-08-30 5 38 42" src="https://user-images.githubusercontent.com/77700130/131264702-d96d4b98-ca75-440d-b34c-be3cc5cf84fa.png">

3. `habitica-task-sync-with-gcal/`配下(`main.py`の存在するディレクトリ)にダウンロードした秘密鍵のファイルを`credentials.json`としてコピーする

## 3. Googleカレンダーへサービスアカウントを登録する
1. 利用するGoogleカレンダーの設定にて、「特定のユーザーとの共有」へ作成したサービスアカウントを追加する
  - サービスアカウントのメールの値を追加する
<img width="608" alt="スクリーンショット 2021-08-30 5 31 04" src="https://user-images.githubusercontent.com/77700130/131264631-9fa92008-33c5-4157-946a-3cdbf2e3f761.png">

## 4.  `main.py`の編集
1. 下記項目を入力する
    - `CALENDAER_ID`は利用するGoogleカレンダーIDを設定
    - `HABITICA_USER_ID` 、`HABITICA_API_TOKEN`はHabiticaの設定、APIページで確認可能

    ``` 
    # 入力する
    CALENDAER_ID = ''
    HABITICA_USER_ID = ''
    HABITICA_API_TOKEN = ''
    ```
<img width="1662" alt="スクリーンショット 2021-08-30 4 10 11" src="https://user-images.githubusercontent.com/77700130/131264623-d26fc060-0d4e-4eb9-b85b-84b189260cac.png">

## 5. デプロイ
1. `gcloud builds submit`コマンドでDockerコンテナをビルドする

    ```
    gcloud builds submit --tag=gcr.io/my-project/image
    ```

    - `my-project`は使用するGCPのプロジェクト
    - `image`は任意のイメージ名
    - 参考
        - https://cloud.google.com/sdk/gcloud/reference/builds/submit

2. Google Cloud Runへデプロイ
    - 下記コマンドでビルドしたDockerコンテナをCloud Runへデプロイする
        - コマンド実行中、Cloud Runでのサービス名、リージョンを設定する

    ```
    gcloud run deploy --image gcr.io/my-project/image
    ```

    - 参考
        - https://cloud.google.com/sdk/gcloud/reference/run

3. HabiticaへWebhook URLを登録する
    - Habiticaの設定、APIページのWebhook URLへ対象Cloud RunのURLを登録する
