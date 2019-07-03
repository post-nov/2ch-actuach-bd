import requests
import asyncio
import aiohttp

from stopwatch import timeit


@timeit
def get_list_of_threads(board):
    data = requests.get(f'https://2ch.hk/{board}/catalog.json').json()
    list_of_threads = []
    for thread in data['threads']:
        list_of_threads.append(f"https://2ch.hk/{board}/res/{(thread['num'])}.json")
    return list_of_threads


async def fetch(session, url):
    async with session.get(url) as response:
        raw_thread = await response.json()
        # pure_thread = thread.cool_posts(raw_thread)
        # if pure_thread != None:
        return raw_thread


async def async_get_raw_threads(board):
    threads = get_list_of_threads(board)
    tasks = []
    async with aiohttp.ClientSession() as session:
        for thread in threads:
            tasks.append(fetch(session, thread))
        res = await asyncio.gather(*tasks)
    return res


@timeit
def get_raw_threads(board):
    raw_threads = asyncio.run(async_get_raw_threads(board))
    return raw_threads


# raw_threads = get_raw_threads('b')
# print(len(raw_threads[0]))
