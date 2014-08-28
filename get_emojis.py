#!/usr/bin/python3

import os
import argparse
import requests
import logging

logging.basicConfig(level=logging.DEBUG, format='%(message)s')


SLACK_URL = 'https://{slack}.slack.com/api/emoji.list?token={token}'


def main(args):
    r = requests.get(SLACK_URL.format(slack=args.slack, token=args.token))
    logging.debug(r.json())
    logging.debug(r.status_code)
    if r.status_code == 200:
        emoji = r.json().get('emoji', {})
        if emoji and not os.path.isdir(args.output):
            os.mkdir(args.output)
        for image_name, image_url in emoji.items():
            logging.debug(image_name)
            logging.debug(image_url)
            if image_url.startswith('alias:'):
                image_url = emoji.get(image_url[6:])
                if not image_url:
                    continue
            image_path = os.path.join(args.output,
                                      image_name + '.' +
                                      image_url.split('.')[-1])
            logging.debug(image_path)
            r = requests.get(image_url, stream=True)
            with open(image_path, 'wb') as f:
                for chunk in r.iter_content():
                    f.write(chunk)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('slack', help='name of your slack group.')
    parser.add_argument('token', help='auth token for slack.')
    parser.add_argument('-o', '--output', help='output location of images',
                        default=os.getcwd())
    args = parser.parse_args()
    main(args)
