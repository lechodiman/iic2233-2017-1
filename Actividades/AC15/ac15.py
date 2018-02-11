import re
import requests
import pickle
import json
import os

with open('AC15.txt', 'r', encoding='utf-8') as file:
    text_lines = file.readlines()
    text = ''
    for line in text_lines:
        text += line

paragraphs = {1: '', 2: '', 3: ''}
i = 1
for line in text_lines:
    paragraphs[i] += line
    if line == '\n':
        i += 1

# remove @
paragraphs = [v for k, v in paragraphs.items()]
new_paragraphs = []
for p in paragraphs:
    new_p = re.sub('@', ' ', p)
    new_paragraphs.append(new_p)

# first paragraph
final_p1 = re.sub('[a-zA-Z]?[0-9]+[a-zA-Z]?', '', new_paragraphs[0])


def fix_first(p):
    pattern = '[a-zA-Z]*[0-9][a-zA-Z]*'
    s = re.sub(pattern, '', p)
    return s


def fix_second(p):
    pattern = '\w*\.correcta\w*'
    corrects = re.findall(pattern, p)
    text = ' '.join(corrects)
    text = re.sub('\.correcta', '', text)
    return text


def fix_third(p):
    pattern = '[a-z\w]*\.[a-z\w]*'
    corrects = re.findall(pattern, p)
    text = ' '.join(corrects)
    text = re.sub('\.', '', text)
    return text

# print(fix_first(new_paragraphs[0]))
# print(fix_second(new_paragraphs[1]))
# print(fix_third(new_paragraphs[2]))

baseurl = 'http://es.wikipedia.org/w/api.php'
my_atts = {'prop': 'extracts', 'action': 'query', 'format': 'json',
           'titles': 'Chile', 'explaintext': ''
           }

while True:
    option = input('Que desea buscar?("quit" to quit) -> ')
    if option == 'quit':
        break

    if option + '.json' in os.listdir():
        # if it was looked before
        with open('{}.json'.format(option), 'r') as file:
            data = json.load(file)
        print(data)
    else:
        # else, make the request
        my_atts['titles'] = option
        resp = requests.get(baseurl, params=my_atts)
        data = resp.json()
        print(data)

        with open('{}.json'.format(option), 'w') as fp:
            json.dump(data, fp)
            print('Datos guardados en base de datos')
