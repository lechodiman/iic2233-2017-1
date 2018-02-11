import requests


def custom_search(query):
    '''Return a url using StackOverflow search engine '''
    google_key = 'AIzaSyBlwS0kkjvxk1CZG77W9LZ4MwIYxYoDsHw'
    url = 'https://www.googleapis.com/customsearch/v1?'
    params = {
        'key': google_key,
        'q': query,
        'cx': '014336879983002060227:ilxot04badm'
    }

    req = requests.get(url, params=params)
    update = req.json()

    url_response = update['items'][0]['link']

    return url_response


def get_error_line(text):
    '''Returns the final line of a Traceback '''
    if '```' in text:
        open_index = text.find('```')
        end_index = text.find('```', open_index + 1)
        code = text[open_index:end_index]
        lines = code.splitlines()
        if 'Traceback' in code:
            error_line = lines[-1]
            return error_line
        else:
            return ''
    else:
        return ''


if __name__ == '__main__':
    print(custom_search('python flask crashes'))
