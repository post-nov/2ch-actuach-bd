from threader import refine_thread
from stopwatch import timeit


@timeit
def get_list_of_cool_posts(raw_threads):
    top_posts = []
    for thread in raw_threads:
        refined_thread = refine_thread(thread)
        for post in refined_thread:
            top_posts.append(post)
    return top_posts
