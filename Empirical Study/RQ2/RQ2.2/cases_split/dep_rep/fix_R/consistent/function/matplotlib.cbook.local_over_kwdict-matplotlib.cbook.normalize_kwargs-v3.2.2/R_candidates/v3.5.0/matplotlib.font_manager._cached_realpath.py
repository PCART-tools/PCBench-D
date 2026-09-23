@lru_cache(64)
def _cached_realpath(path):
    return os.path.realpath(path)
