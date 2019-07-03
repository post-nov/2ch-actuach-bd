import time


def timeit(function):

    def wrapper(*args, **kwargs):
        start = time.time()
        result = function(*args, **kwargs)
        interval = time.time() - start
        print(f"Function \"{function.__name__}\" executed for {round(interval, 3)} seconds")
        return result

    return wrapper
