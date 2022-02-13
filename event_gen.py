from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from prometheus_client import Summary

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 5 events')
        
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=5, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        '''# Prints the start and name of the next 10 events
        # for event in events:
        #     start = event['start'].get('dateTime', event['start'].get('date'))
        #     print(start, event['summary'])
        '''
        
        create_event(service, 'test')
        create_reach_out_to_friend_event(service, 'friend')

    except HttpError as error:
        print('An error occurred: %s' % error)

def create_reach_out_to_friend_event(service, type):
    

    EVENT = {}
    pass

def create_event(service, type):
    if type == 'test':
        """ Creates a test event for the HH Calendar """
        # This calendarID is for my HH Calendar specifically, not my primary
        # ip1f8ub1q7lrr8eppv8jd9cc4c@group.calendar.google.com
        GMT_OFF = '-07:00' # PDT/MST/GMT-7
        EVENT = {
            'summary': 'Calendar event from API - visibility test',
            'start': {'dateTime': '2022-02-13T18:00:00%s' % GMT_OFF, 'timeZone': 'America/Chicago'},
            'end': {'dateTime': '2022-02-13T19:00:00%s' % GMT_OFF, 'timeZone': 'America/Chicago'},
            'visibility': 'private',
        }
    e = service.events().insert(calendarId='ip1f8ub1q7lrr8eppv8jd9cc4c@group.calendar.google.com', 
        body=EVENT).execute()
    
    print('''*** %r event added:
        Start: %s
        End: %s''' % (e['summary'].encode('utf-8'), e['start']['dateTime'], e['end']['dateTime']))


if __name__ == '__main__':
    main()

