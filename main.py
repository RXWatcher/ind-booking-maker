import sys
import time
from datetime import datetime

from utils import parse_args, load_yaml
from ind_api import get_ind_data, make_ind_appointment, make_ind_reservation

import telebot


args = parse_args()
config, error = load_yaml(args.config)
if error is not None:
    print(error)
    sys.exit(1)
bot = telebot.TeleBot(config['telegram']['token'], parse_mode='MARKDOWN')


def check():
    date_format = '%Y-%m-%d'
    date_from = datetime.strptime(config['date_from'], date_format)
    date_to = datetime.strptime(config['date_to'], date_format)

    data, error = get_ind_data(config['office'], config['product'])
    if error is not None:
        print('Failed to get data')
        sys.exit(1)

    found = False
    for item in data:
        print(item)
        date = datetime.strptime(item['date'], '%Y-%m-%d')
        if date >= date_from and date <= date_to:
            found = True
            appointment_url = f'https://oap.ind.nl/oap/en/#/{ config["product"] }'
            line = 'Found an IND slot: {}, {}\n{}\n{}'.format(item['date'], item['startTime'], item['key'], appointment_url)
            print(line)
            bot.send_message(config['telegram']['chat_id'], line)

            res, error = make_ind_reservation(config['office'], item)
            if error is not None:
                line = 'Failed to make a reservation\nStatus code: {}\nError: {}'.format(error, res['data'])
                print(line)
                bot.send_message(config['telegram']['chat_id'], line)
                continue

            res, error = make_ind_appointment(config['office'], config['product'], item, config['book_data'])
            if error is not None:
                line = 'Failed to make a appointment\nStatus code: {}\nError: {}'.format(error, res['data'])
                print(line)
                bot.send_message(config['telegram']['chat_id'], line)
                continue
            else:
                print('Appointment made!')
                cancelation_url = 'https://oap.ind.nl/oap/en/#/cancel/{}'.format(res['data']['key'])
                line = 'Appointment made!\nDate: {} {}\nCode: {}\nKey: {}\n[Cancelation link]({})'.format(
                    res['data']['date'], res['data']['startTime'], res['data']['code'], res['data']['key'], cancelation_url
                )
                print(line)
                bot.send_message(config['telegram']['chat_id'], line)
                sys.exit(0)
    if not found:
        print('Found nothing')


def main():
    time_sleep = int(config['time_sleep'])
    while True:
        print('Checking...')
        check()
        print('Waiting for {} seconds'.format(time_sleep))
        time.sleep(time_sleep)


if __name__ == '__main__':
    main()
