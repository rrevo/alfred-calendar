#!/usr/bin/env python3

import glob
import json
import os
import os.path
import subprocess
from datetime import datetime, timedelta

from event import Event


CALENDAR_DB_DIR = os.path.expanduser(os.path.join(
    '~', 'Library', 'Calendars'))

# How many minutes before or into the meeting to show the conference URL
TIME_THRESHOLD_MINS = 20


def get_event_uids():

    event_uids = subprocess.check_output([
        'osascript',
        'get-event-uids.applescript'
    ]).decode('utf-8').replace('.', '').strip().split(',')

    if len(event_uids) == 1 and event_uids[0] == '':
        return []
    else:
        return event_uids


def get_event_path(event_uid):
    normalized_event_uid = event_uid.replace('.', '')
    event_filename = f'{normalized_event_uid}.ics'
    event_paths = glob.glob(os.path.join(
        CALENDAR_DB_DIR, '*', '*', 'Events', event_filename))
    if event_paths:
        return event_paths[0]
    else:
        return None


def get_event(event_path):
    with open(event_path, 'r') as event_file:
        return Event(event_file.read())


def is_time_within_range(event_datetime):
    current_datetime = datetime.now().astimezone()
    threshold = timedelta(minutes=TIME_THRESHOLD_MINS)
    min_datetime = (event_datetime - threshold)
    max_datetime = (event_datetime + threshold)
    if min_datetime <= current_datetime <= max_datetime:
        return True
    else:
        return False


def main():

    feedback = {
        'items': []
    }

    for event_uid in get_event_uids():
        event_path = get_event_path(event_uid)
        event = get_event(event_path)
        if not event.conference_url:
            continue
        if not is_time_within_range(event.start_datetime_local):
            continue
        feedback['items'].append({
            'title': event.summary,
            'subtitle': event.start_datetime_local.strftime('%-I:%M%p').lower(),
            'text': {
                'copy': event.conference_url,
                'largetype': event.conference_url
            },
            'variables': {
                'event_summary': event.summary,
                'event_conference_url': event.conference_url
            }
        })

    if not feedback['items']:
        feedback['items'].append({
            'title': 'No Results',
            'subtitle': 'No calendar events could be found',
            'valid': 'no'
        })

    print(json.dumps(feedback, indent=2))


if __name__ == '__main__':
    main()
