#!/usr/bin/python3

import os
import argparse
import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')


SLACK_URL = 'https://{slack}.slack.com/api/emoji.list'


def download_image(url, path):
    r = requests.get(url, stream=True)
    with open(path, 'wb') as f:
        for chunk in r.iter_content():
            f.write(chunk)


def reconcile_aliases(image_url, emoji):
    if image_url.startswith('alias:'):
        image_url = emoji.get(image_url[6:], None)
    return image_url


def main(args):
    params = {'token': args.token}
    r = requests.get(SLACK_URL.format(slack=args.slack), params=params)
    if r.status_code == 200:
        emoji = r.json().get('emoji', {})
        if emoji and not os.path.isdir(args.output):
            os.mkdir(args.output)
        for image_name, image_url in emoji.items():
            image_url = reconcile_aliases(image_url, emoji)
            if not image_url:
                continue
            image_ext = image_url.split('.')[-1]
            image_path = os.path.join(args.output,
                                      image_name + '.' + image_ext)
            if args.trample or not os.path.exists(image_path):
                download_image(image_url, image_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('slack', help='name of your slack group.')
    parser.add_argument('token', help='auth token for slack.')
    parser.add_argument('-o', '--output', help='output location of images',
                        default=os.getcwd())
    parser.add_argument('--trample',
                        help='replace / redownload images even if one exists',
                        action='store_true')
    args = parser.parse_args()
    main(args)
