@functools.lru_cache(4096)
def print_once(*args):
    print(*args)
