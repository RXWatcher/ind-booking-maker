import argparse
from urllib import request, parse
from urllib.parse import quote_plus

import requests
from ruamel.yaml import YAML


def parse_args():
    # command-line arguments of the program
    parser = argparse.ArgumentParser(description='Process a config file')
    parser.add_argument('config', type=str, help='config file to read the data from')
    return parser.parse_args()


def telegram_send(line, token, chat_id):
    url = f"https://api.telegram.org/bot{token}/sendmessage?chat_id={chat_id}&parse_mode=markdown&text={quote_plus(line)}"   
    response=requests.post(url)
    return response.text


def load_yaml(path, key=None):
    try:
        with open(path, 'r') as f:
            yaml = YAML()
            try:
                data = yaml.load(f.read())
                if key is None:
                    return data, None
                else:
                    return data.get(key), None
            except yaml.YAMLError as e:
                return None, e
    except FileNotFoundError as e:
        return None, e
