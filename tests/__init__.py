#!/usr/bin/env python3

import os


os.environ['conference_domains'] = '*.zoom.us, zoom.us, meet.google.com, hangouts.google.com, *.microsoft.com, meet.goto.com, *.webex.com, webex.com, meetings.dialpad.com'  # noqa
os.environ['calendar_names'] = ''
os.environ['use_direct_zoom'] = 'false'
os.environ['use_direct_msteams'] = 'false'
os.environ['event_time_threshold_mins'] = '20'
