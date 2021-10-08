from __future__ import print_function
import os.path
from datetime import datetime, timezone

from googleapiclient.discovery import build
import google.auth
import flask
import requests

app = flask.Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/calendar']

# 入力する
CALENDAER_ID = ''
HABITICA_USER_ID = ''
HABITICA_API_TOKEN = ''


@app.route('/taskactivity', methods=['POST'])
def webhook():
    # Request contains data as shown at https://habitica.com/apidoc/#api-Webhook
    try:
        task_title = get_task_title()
        print(task_title)
        event_data = create_event_data(task_title)
        creds = google.auth.load_credentials_from_file(
            './credentials.json', SCOPES)[0]
        service = build('calendar', 'v3', credentials=creds)
        # service = googleapiclient.discovery.build('calendar', 'v3', credentials=gapi_creds)
        result = service.events().insert(calendarId=CALENDAER_ID, body=event_data).execute()
        print('OK:  ' + result['htmlLink'])

        return '', 200
    except Exception as e:
        print(e)
        return '', 500


# タスク詳細をhabiticaへ問い合わせて取得する
def get_task_title():
    auth_headers = {'x-api-user': HABITICA_USER_ID,
                    'x-api-key': HABITICA_API_TOKEN}
    event_id = flask.request.json['task']['id']
    url = 'https://habitica.com/api/v3/tasks/' + event_id

    try:
        r = requests.get(url, headers=auth_headers, timeout=(10))
        r = r.json()
        return r['data']['text']
    except Exception:
        return "[ERROR] can't get the task title."


# Google Calendarへ登録するイベント情報を生成する
def create_event_data(task_title):

    # updated_at = flask.request.json['task']['updatedAt']
    updated_at = str(datetime.now(
        timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))

    event = {
        'summary': task_title,
        'description': flask.request.json['task']['id'],
        'start': {
            'dateTime': updated_at,
            'timeZone': 'Asia/Tokyo',
        },
        'end': {
            'dateTime': updated_at,
            'timeZone': 'Asia/Tokyo',
        },
    }

    if (flask.request.json['task']['type']) == "habit":
        event['summary'] = task_title
    elif (flask.request.json['task']['type']) == "daily":
        event['summary'] = task_title
    elif (flask.request.json['task']['type']) == "todo":
        event['summary'] = task_title
    else:
        event['summary'] = 'タイトル未取得'

    return event


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get('PORT', 8080)))
