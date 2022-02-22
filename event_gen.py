from __future__ import print_function

import random
import datetime
from datetime import date
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
        type = input('What type of event would you like to generate? friend or family?')

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

        create_event(service, type)

    except HttpError as error:
        print('An error occurred: %s' % error)

def create_event(service, type):
    EVENT = create_event_details(type)
    
    e = service.events().insert(calendarId='ip1f8ub1q7lrr8eppv8jd9cc4c@group.calendar.google.com', 
        body=EVENT).execute()
    
    print('''*** %r event added:
        Start: %s
        End: %s''' % (e['summary'].encode('utf-8'), e['start']['date'], e['end']['date']))

def create_event_details(type):
    EVENT = {}
    time = select_random_date(type)
    summary = 'blank'

    if type == 'test':
        summary = 'Just a test event'
    if type == 'friend':
        summary = 'You should reach out to a friend'
    if type == 'family':
        summary ='Reach out to Jack or Parents this week',

    EVENT = {
            'summary': summary,
            'start': time,
            'end': time,
            'visibility': 'private',
        }
    return EVENT

def select_random_date(type):
    #Change this to just increment a certain amount of months based on what type of event, 
    #then apply that to the start date
    months_to_increment = 1

    # Need to take into account rollover into the next year
    if type == 'test':
        today = date.today()
    if type == 'friend':
        months_to_increment = 2
    if type == 'family':
        months_to_increment = 1
    if type == 'gift':
        months_to_increment = 3

    rand_day = random.randint(1, 28)
    rand_month = random.randint(1, months_to_increment)

    time = date.today().replace(day=rand_day)
    time = time.replace(month=time.month+rand_month)
    time = str(time)

    return_time = {'date': time}
    
    return return_time


if __name__ == '__main__':
    main()

