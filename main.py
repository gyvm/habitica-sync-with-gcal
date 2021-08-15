from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from flask import Flask, request


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/taskactivity', methods=['POST'])
def webhook():
    
    try:
        # Request contains data as shown at https://habitica.com/apidoc/#api-Webhook
        if request.is_json == True:
            if request.json['webhookType'] == "taskActivity":
                event_data = create_event_data()
                creds = init_service()
                service = build('calendar', 'v3', credentials=creds)
                insert_gcal_event(service, event_data)
                
                return '', 200
    except Exception as e:
        print(e)
        return '', 500

def create_event_data():
    task_title = request.json['task']['text']
    task_id = 'task_id: ' + request.json['task']['id']
    updated_date =request.json['task']['updatedAt']
    
    event = {
        'summary': task_title,
        'description': task_id,
        'start': {
            'dateTime': updated_date,
            'timeZone': 'Asia/Tokyo',
        },
        'end': {
            'dateTime': updated_date,
            'timeZone': 'Asia/Tokyo',
        },
    }
    
    if (request.json['task']['type']) == "habit":
        task_title = "[habit] " + task_title
    elif (request.json['task']['type']) == "daily":
        task_title = "[habit] " + task_title
    elif (request.json['task']['type']) == "todo":
        task_title = "[habit] " + task_title
    else:
        task_title = "[error] タイトル未取得"

    print(event)
    return event

def init_service():
    # See "https://developers.google.com/docs/api/quickstart/python" for more information
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

def insert_gcal_event(service, event):
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get('PORT', 8080)))
