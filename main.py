# coding: utf8
import requests
import re
import json
import os
from datetime import datetime


def get_list_of_threads(num=-1):
    data = requests.get('https://2ch.hk/b/catalog.json').json()
    list_of_threads = []
    for thread in data['threads']:
        list_of_threads.append(int(thread['num']))

    return list_of_threads[:num]


def unix_to_human(timestamp):
    return (datetime.utcfromtimestamp(timestamp).strftime('%d-%m-%y %H:%M'))


def clean_string(string):
    to_delete = {
        '<br>': '\n',
        '&#47;': '/',
        '&gt;': '',
        '&#39;': '',
        '"': '',
        '&quot;': '"',
        '<span class=unkfunc>': '>',
        '?&lt;': '<',
        '&#92;': '\\'
    }

    for fr_, to_ in to_delete.items():
        string = string.replace(fr_, to_)

    string = re.sub(r'<.*?>', r'', string)
    return string


def content_of_thread(op_number):
    thread = requests.get(f'https://2ch.hk/b/res/{op_number}.json').json()
    dict_of_posts = {}
    posts = thread['threads'][0]['posts']
    for post in posts:
        post_number = post['num']
        dict_of_posts[post_number] = {
            'content': clean_string(post['comment']),
            'date': unix_to_human(post['timestamp']),
            'notions': 0,
            'is_op': False,
            'link': f'https://2ch.hk/b/res/{op_number}.html#{post_number}'
        }

        if post_number == op_number:
            dict_of_posts[post_number]['is_op'] = True

    for post_num in dict_of_posts.keys():
        for post in dict_of_posts.values():
            if ('>>'+str(post_num)) in post['content']:
                dict_of_posts[post_num]['notions'] += 1

    return dict_of_posts


def get_cool_posts(list_of_threads, amount=None):
    if amount == None:
        amount = (len(list_of_threads))
    cool_posts = {}
    for op_num in range(amount):
        try:
            thread = content_of_thread(list_of_threads[op_num])
            for post, value in thread.items():
                if value['notions'] > 4:
                    cool_posts[post] = thread[post]
            print('Processed: ', op_num+1, '/', amount, sep='')
        except:
            print('Failed at', f'https://2ch.hk/b/res/{op_num}.html')
    print('Finished. Number of posts:',
          len(cool_posts), '\n------------------------\n')
    return cool_posts


def show_tooked(posts):
    for post, value in posts.items():
        print(f'Актуальный пост №{post}:', end='')
        if not value['is_op']:
            print('(Пост крутой, а не ОПычный)')
        print('\n\n', value['content'], sep='', end='')
        print('\n\n\nБыл упомянут', value['notions'],
              'раз(а). Отправлен', value['date'])
        print('Ссылка:\n', value['link'], sep='')
        print('*********************************\n')


if __name__ == '__main__':

    list_of_threads = get_list_of_threads()
    x = get_cool_posts(list_of_threads)
    # show_tooked(x)

    try:
        with open('thread_dump.json', 'r') as json_file:
            j = json.load(json_file)
    except:
        j = {}
        for key, value in x.items():
            j[key] = value


    with open('thread_dump.json', 'w') as json_file:
        json.dump(j, json_file)
