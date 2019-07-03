import time

from downloader import get_raw_threads
from picker import get_list_of_cool_posts
from db_manager import update_database
from settings import (BOARD,
                      USER,
                      PASSWORD,
                      DATABASE)


if __name__ == "__main__":
    for i in range(10):
        raw_threads = get_raw_threads(BOARD)
        top_posts = get_list_of_cool_posts(raw_threads)
        update_database(top_posts)
        time.sleep(600)
