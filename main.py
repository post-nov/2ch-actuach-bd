# coding: utf8
import requests
import re
import json
import os
from datetime import datetime
import psycopg2

DB_NAME = "2ch_posts"
DB_USER = "postgres"
DB_PASSWORD = "password"

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

class DB():

    def __init__(self):
        self.conn = psycopg2.connect(f"dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD}")
        self.cur = self.conn.cursor()

    def pass_params(self, dict_values):
        content_db = dict_values['content']
        date_db = dict_values['date']
        notions_db = dict_values['notions']
        is_op_db = dict_values['is_op']
        link_db = dict_values['link']

        self.cur.execute(f"""
            INSERT INTO posts (content, date, notions, is_op, link) 
            VALUES ('{content_db}', '{date_db}', '{notions_db}', '{is_op_db}', '{link_db}')
            """)
        self.conn.commit()

    def count_posts(self):
        self.cur.execute("SELECT COUNT(*) FROM posts")
        return self.cur.fetchone()

    def close(self):
        self.cur.close()
        self.conn.close()    


def get_cool_posts(list_of_threads, amount=None):
    if amount == None:
        amount = (len(list_of_threads))

    postgres = DB()

    for op_num in range(amount):
        try:
            thread = content_of_thread(list_of_threads[op_num])
            for post, value in thread.items():
                if value['notions'] > 4:
                    params = thread[post]
                    postgres.pass_params(params)
            print('Processed: ', op_num+1, '/', amount, sep='')
        except:
            print('Failed at', f'https://2ch.hk/b/res/{list_of_threads[op_num]}.html')
    postgres.close()


if __name__ == '__main__':

    list_of_threads = get_list_of_threads()
    x = get_cool_posts(list_of_threads)

    test = DB()
    print(test.count_posts()[0])
    test.close()
