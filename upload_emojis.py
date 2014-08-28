#!/usr/bin/python3

# import os
# import argparse
import requests
from requests_toolbelt import MultipartEncoder
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

SLACK_URL = 'https://{slack}.slack.com/customize/emoji'

m = MultipartEncoder(fields={'name': 'test',
                             'add': '1',
                             'crumb': 's-1409258775-601ccd1bed-☃',
                             'img': ('filename',
                                     open('images/alec.jpg', 'rb'),
                                     'image/jpeg')
                             }
                     )

r = requests.post(SLACK_URL.format(slack='grandrapids'), data=m,
                  headers={'Content-Type': m.content_type})
print(r.status_code)
print(r)
