from flask import Flask, request
import requests
import json
from github_api import (get_issue, post_comment, close_issue,
                        add_label, format_issue, get_comments,
                        get_labels)
from google_api import custom_search, get_error_line
from air_quality import get_air_status

bot_token = '364223999:AAFf1yPOvBHyoUKjRZZibixfQ655KTHoEKQ'
url = 'https://api.telegram.org/bot{}'.format(bot_token)
CHAT_ID_SET = set()


def send_to_list(chat_id_set, message):
    for chat_id in chat_id_set:
        send_message(chat_id, message)


def send_message(chat_id, message):
    '''Sends a message using Chodibot's Telegram account '''
    args = {'chat_id': chat_id, 'text': message}
    requests.get(url + '/sendmessage', params=args)


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        update = request.get_json(force=True)
        chat_id = update['message']['chat']['id']
        message = update['message']['text']

        if message == '/send_test':
            send_message(chat_id, 'test, your id: {}'.format(chat_id))
        elif message == '/send_hi':
            send_message(chat_id, 'hi')
        elif message.startswith('/get'):
            message_split = message.split(' ')
            if len(message_split) != 2:
                send_message(chat_id, 'Not enough arguments')
                return 'Hi there'
            num_issue = message_split[1]
            if num_issue.startswith('#'):
                num_issue = int(num_issue.replace('#', ''))
                issue_req = get_issue(num_issue)
                if issue_req.status_code == 200:
                    issue = issue_req.json()
                    send_message(chat_id, format_issue(issue))
                else:
                    send_message(chat_id, 'It was not possible to get issue')
            else:
                send_message(chat_id, 'Num issue must start with #')
        elif message.startswith('/post'):
            message_split = message.split(' ', maxsplit=2)
            if len(message_split) != 3:
                send_message(chat_id, 'Not enough arguments')
                return 'Hi there'
            num_issue = message_split[1]
            respuesta = message_split[2]
            if not num_issue.startswith('#') or not respuesta.startswith('*'):
                send_message(chat_id, 'Check # and *')
            else:
                num_issue = int(num_issue.replace('#', ''))
                respuesta = respuesta.replace('*', '')
                req = post_comment(num_issue, respuesta)
                if req.status_code == 201:
                    send_message(chat_id, 'Comment posted')
                else:
                    send_message(chat_id, 'It was not possible to post comment')
        elif message.startswith('/label'):
            message_split = message.split(' ')
            if len(message_split) != 3:
                send_message(chat_id, 'Not enough arguments')
                return 'Hi there'
            num_issue = message_split[1]
            label = message_split[2]
            if num_issue.startswith('#'):
                num_issue = int(num_issue.replace('#', ''))
                if label in get_labels(num_issue, only_names=True):
                    send_message(chat_id, 'Issue already has this label')
                else:
                    req = add_label(num_issue, label)
                    if req.status_code == 200:
                        send_message(chat_id, 'Label added')
                    else:
                        send_message(chat_id, 'It was not possible to add label')
            else:
                send_message(chat_id, 'Num issue must start with #')
        elif message.startswith('/close'):
            message_split = message.split(' ')
            if len(message_split) != 2:
                send_message(chat_id, 'Not enough arguments')
                return 'Hi there'
            num_issue = message_split[1]
            if num_issue.startswith('#'):
                num_issue = int(num_issue.replace('#', ''))
                issue = get_issue(num_issue).json()
                if issue['state'] == 'closed':
                    send_message(chat_id, 'Issue already closed')
                else:
                    req = close_issue(num_issue)
                    if req.status_code == 200:
                        send_message(chat_id, 'Issue closed')
                    else:
                        send_message(chat_id, 'It was not possible to close the issue')
            else:
                send_message(chat_id, 'Num issue must start with #')
        elif message == '/add':
            if chat_id in CHAT_ID_SET:
                send_message(chat_id, 'You are already in contacts')
            else:
                CHAT_ID_SET.add(chat_id)
                send_message(chat_id, 'You were added to contacts')
        elif message == '/remove':
            if chat_id in CHAT_ID_SET:
                CHAT_ID_SET.remove(chat_id)
                send_message(chat_id, 'You were removed from contacts')
            else:
                send_message(chat_id, 'You are not in the contacts')
        elif message == '/air':
            send_message(chat_id, get_air_status())
        else:
            send_message(chat_id, 'Default')

        return 'Received : {}'.format(message)
    else:
        return 'Hi there'


@app.route('/github_handler', methods=['GET', 'POST'])
def github_handler():
    if request.method == 'POST':
        update = request.get_json(force=True)
        action = update['action']
        issue = update['issue']

        formated_issue = format_issue(issue)

        message_to_send = ''
        message_to_send += '[Action: {}]'.format(action) + '\n\n'
        message_to_send += formated_issue

        send_to_list(CHAT_ID_SET, message_to_send)

        if action == 'opened':
            error_line = get_error_line(issue['body'])
            if error_line != '':
                help_url = custom_search('python ' + error_line)
                issue_num = issue['number']
                post_comment(issue_num, 'This might help: {}'.format(help_url))
        elif action == 'closed':
            issue_author = issue['user']['login']
            issue_num = issue['number']
            comments = get_comments(issue_num).json()
            if len(comments) != 0 and \
                    comments[0]['user']['login'] == 'Chodibot'\
                    and comments[0]['body'].startswith('This might help: '):

                comments_authors = set([c['user']['login'] for c in comments])
                if comments_authors == {issue_author, 'Chodibot'} or comments_authors == {'Chodibot'}:
                    add_label(issue_num, 'Googleable')

        return 'Hi there i am a github handler'
    else:
        return 'You are probably using GET'
