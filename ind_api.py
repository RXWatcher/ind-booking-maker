import json

import requests


def parse_response(line):
    if line is None:
        return None
    try:
        data = json.loads(line.split('\n')[1])
        return data
    except json.decoder.JSONDecodeError:
        return None


def get_ind_data(office, product):
    url = f'https://oap.ind.nl/oap/api/desks/{office}/slots/?productKey={product}&persons=1'
    res = requests.get(url)
    data = parse_response(res.text)
    return data['data'], None if res.status_code == 200 else res.status_code


def make_ind_reservation(office, info):
    url = 'https://oap.ind.nl/oap/api/desks/{}/slots/{}'.format(office, info['key'])
    payload = {
        'date': info['date'],
        'startTime': info['startTime'],
        'endTime': info['endTime'],
        'key': info['key'],
        'parts': 1
    }
    res = requests.post(url, json=payload)
    data = parse_response(res.text)
    return data, None if res.status_code == 200 else res.status_code


def make_ind_appointment(office, product, info, book_data):
    payload = {
        'bookableSlot': {
            'key': info['key'],
            'date': info['date'],
            'startTime': info['startTime'],
            'endTime': info['endTime'],
            'parts': info['parts'],
            'booked': False
        },
        'appointment': {
            'productKey': product,
            'date': info['date'],
            'startTime': info['startTime'],
            'endTime': info['endTime'],
            'email': book_data['email'],
            'phone': book_data['phone'],
            'language': 'en',
            'customers': [{
                'vNumber': book_data['vNumber'],
                'bsn': book_data['bsn'],
                'firstName': book_data['firstName'],
                'lastName': book_data['lastName']
            }]
        }
    }
    url = f'https://oap.ind.nl/oap/api/desks/{office}/appointments/'
    res = requests.post(url, json=payload)
    data = parse_response(res.text)
    return data, None if res.status_code == 200 else res.status_code