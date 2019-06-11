import requests
import datetime
from time import sleep

url = "https://api.telegram.org/bot783040952:AAFUDFhHTvob4yV3uitVXmS1Hgat_xZJ8nQ/"


def get_updates_json(request):
    params = {'timeout': 100, "offset": None}
    response = requests.get(request + 'getUpdates')
    return response.json()


def last_update(data):  
    results = data['result']
    total_updates = len(results) - 1
    return results[total_updates]


def get_chat_id(update):
    chat_id = update['message']['chat']['id']
    return chat_id

def send_msg(chat, text):
    params = {'chat_id': chat, 'text': text}
    response = requests.post(url + 'sendMessage', data=params)
    return response


def main():
    update_id = last_update(get_updates_json(url))['update_id']
    while True:
        if update_id == last_update(get_updates_json(url))['update_id']:
            send_msg(get_chat_id(last_update(get_updates_json(url))), 'test')
            update_id += 1
        sleep(1)


if __name__ == '__main__':
    main()


#chat_id = get_chat_id(last_update(get_updates_json(url)))
#send_msg(chat_id, 'Hello World') to get an update and send a message yourself