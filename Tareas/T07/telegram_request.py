import requests

bot_token = '364223999:AAFf1yPOvBHyoUKjRZZibixfQ655KTHoEKQ'
url = 'https://api.telegram.org/bot{}'.format(bot_token)
update = requests.get(url + '/getupdates').json()
chat_id = update['result'][0]['message']['chat']['id']
print(chat_id)

# send message
text = 'test'
args = {'chat_id': chat_id, 'text': text}
requests.get(url + '/sendmessage', params=args)
