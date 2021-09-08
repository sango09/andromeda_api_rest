"""Google Calendar API."""

# Utilidades
from __future__ import print_function

import os
from datetime import datetime

# Django
from django.conf import settings
# Google Calendar
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.discovery_cache.base import Cache

# Modelos
from andromeda.users.models import User


class MemoryCache(Cache):
    _CACHE = {}

    def get(self, url):
        return MemoryCache._CACHE.get(url)

    def set(self, url, content):
        MemoryCache._CACHE[url] = content


def schedule_service(
    summary,
    location,
    comments,
    event_date,
    calendar_id,
    update_event=None,
    event_id=None
):
    """Crea el evento en google calendar con los datos proporcionados."""
    assistans_emails = [{'email': i.email} for i in User.objects.filter(is_assistant=True)]
    year = int(event_date.strftime('%Y'))
    month = int(event_date.strftime('%m'))
    day = int(event_date.strftime('%d'))
    hour = int(event_date.strftime('%H'))
    minute = int(event_date.strftime('%M'))

    event = {
        'summary': summary,
        'location': location,
        'description': comments,
        'start': {
            'dateTime': datetime(year, month, day, hour, minute, 0).isoformat(),
            'timeZone': 'UTC-5',
        },
        'end': {
            'dateTime': datetime(year, month, day, hour, minute, 0).isoformat(),
            'timeZone': 'UTC-5',
        },
        'attendees': assistans_emails,
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    if update_event is True:
        return google_calendar_service(calendarBody=event,
                                       calendar=calendar_id,
                                       calendarUpdate=True,
                                       eventId=event_id)
    else:
        return google_calendar_service(calendarBody=event,
                                       calendar=calendar_id,
                                       calendarInsert=True)


def google_calendar_service(
    calendar,
    calendarBody=None,
    eventId=None,
    calendarInsert=None,
    calendarUpdate=None,
    calendarDelete=None,
):
    """Configuracion para Google Calendar API."""
    creds = None
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    token_json = settings.APPS_DIR / 'tasks/google_calendar/token.json'

    if os.path.exists(token_json):
        creds = Credentials.from_authorized_user_file(token_json, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            credentials_path = settings.APPS_DIR.path('tasks/google_calendar/credentials.json')
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_json, 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds, cache=MemoryCache())

    if calendarInsert is True:
        event = service.events().insert(calendarId=calendar,
                                        body=calendarBody,
                                        sendUpdates='none',
                                        ).execute()
        return event.get('id')

    if calendarUpdate is True:
        service.events().update(calendarId=calendar,
                                eventId=eventId,
                                body=calendarBody,
                                sendUpdates='none',
                                ).execute()
    if calendarDelete is True:
        service.events().delete(calendarId=calendar,
                                eventId=eventId,
                                sendUpdates='none',
                                ).execute()
