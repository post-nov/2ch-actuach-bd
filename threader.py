# coding: utf8
from datetime import datetime
import re
import time


def unix_to_human(timestamp):
    return (datetime.utcfromtimestamp(timestamp).strftime('%d-%m-%y %H:%M'))


def clean_string(string):
    to_replace = {
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

    for fr_, to_ in to_replace.items():
        string = string.replace(fr_, to_)
    string = re.sub(r'<.*?>', r'', string)
    return string


def get_clean_post(op_number, post):
    post_number = post['num']
    files = [('https://2ch.hk'+file['path'])
             for file in post['files']]
    thumbs = [('https://2ch.hk'+file['thumbnail'])
              for file in post['files']]
    post = {
        'number': post_number,
        'content': clean_string(post['comment']),
        'date': unix_to_human(post['timestamp']),
        'notions': 0,
        'is_op': False,
        'link': f'https://2ch.hk/b/res/{op_number}.html#{post_number}',
        'files': files,
        'thumbs': thumbs
    }
    return post


def remove_not_cool(op_number, thread):
    for post_num in thread.keys():
        if post_num == op_number:
            thread[post_num]['is_op'] = True
        for post in thread.values():
            if ('>>'+str(post_num)) in post['content']:
                thread[post_num]['notions'] += 1
    thread = {k: v for k, v in thread.items() if v['notions'] > 4}
    cool_posts = list(thread.values())
    return cool_posts


def refine_thread(raw_thread):
    # start = time.time()
    op_number = raw_thread['threads'][0]['posts'][0]['num']
    thread = {}

    for post in raw_thread['threads'][0]['posts']:
        thread[post['num']] = get_clean_post(op_number, post)
    # print(f'Thread >>{op_number} took', time.time() - start)
    purified = remove_not_cool(op_number, thread)
    return purified
