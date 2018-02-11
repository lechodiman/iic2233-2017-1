import json
import requests

credentials = ('Chodibot', 'chodibotnofakepassword')


def print_pretty(jsonstring, indent=4, sort_keys=False):
    print(json.dumps(jsonstring, indent=indent, sort_keys=sort_keys))


def get_issue(number):
    '''
    Gets an issue by its number
    Returns the issue itself
    '''
    owner = 'lechodiman'
    repo = 'dummy_repo'
    url = "https://api.github.com/repos/{}/{}/issues/{}".format(owner, repo, number)

    req = requests.get(url)
    return req


def post_comment(number, comment):
    '''Posts a comment using ChodiBot's GitHub account '''
    owner = 'lechodiman'
    repo = 'dummy_repo'
    url = "https://api.github.com/repos/{}/{}/issues/{}/comments".format(owner, repo, number)
    params = {
        'body': comment
    }

    req = requests.post(url, data=json.dumps(params), auth=credentials)
    return req


def get_comments(number):
    '''Returns list of comments in the issue '''
    owner = 'lechodiman'
    repo = 'dummy_repo'
    url = "https://api.github.com/repos/{}/{}/issues/{}/comments".format(owner, repo, number)
    req = requests.get(url, auth=credentials)
    return req


def post_issue(title, body):
    '''
    Posts an issue using ChodiBot's GitHub account
    Returns the issue itself
    '''
    owner = 'lechodiman'
    repo = 'dummy_repo'
    url = "https://api.github.com/repos/{}/{}/issues".format(owner, repo)
    params = {
        'title': title,
        'body': body,
        'asignee': 'Chodibot'
    }

    req = requests.post(url, data=json.dumps(params), auth=credentials)
    return req


def close_issue(number):
    '''
    Closes an issue in dummy_repo
    Returns the issue itself
    '''
    owner = 'lechodiman'
    repo = 'dummy_repo'
    url = "https://api.github.com/repos/{}/{}/issues/{}".format(owner, repo, number)
    params = {
        'asignee': 'Chodibot',
        'state': 'closed'
    }

    req = requests.patch(url, data=json.dumps(params), auth=credentials)
    return req


def add_label(number, label):
    '''
    Adds a label to an issue in dummy_repo
    Returns list of labels in the issue.
    '''
    owner = 'lechodiman'
    repo = 'dummy_repo'
    url = "https://api.github.com/repos/{}/{}/issues/{}/labels".format(owner, repo, number)
    params = [label]

    req = requests.post(url, data=json.dumps(params), auth=credentials)
    return req


def get_labels(number, only_names=False):
    '''
    Returns a list of labels for an issue(request object). If only_names=True
    then returns a python list with the names of the labels.
    '''
    owner = 'lechodiman'
    repo = 'dummy_repo'
    url = "https://api.github.com/repos/{}/{}/issues/{}/labels".format(owner, repo, number)

    req = requests.get(url, auth=credentials)

    if only_names:
        return [label['name'] for label in req.json()]
    else:
        return req


def format_issue(issue):
    '''Returns formated string with issue contents '''
    user_login = issue['user']['login']
    number = issue['number']
    title = issue['title']
    body = issue['body']
    html_url = issue['html_url']

    formated = ''
    formated += '[{}]'.format(user_login) + '\n\n'
    formated += '[#{} - {}]'.format(number, title) + '\n\n'
    formated += '{}'.format(body) + '\n\n'
    formated += '[Link: {}]'.format(html_url)

    return formated


if __name__ == '__main__':
    print(get_labels(3, only_names=True))
