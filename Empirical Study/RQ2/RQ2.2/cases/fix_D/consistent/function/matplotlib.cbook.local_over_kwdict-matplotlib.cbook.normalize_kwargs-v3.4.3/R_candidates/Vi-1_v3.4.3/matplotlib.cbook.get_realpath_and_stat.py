@_api.deprecated("3.3", alternative="os.path.realpath and os.stat")
@functools.lru_cache()
def get_realpath_and_stat(path):
    realpath = os.path.realpath(path)
    stat = os.stat(realpath)
    stat_key = (stat.st_ino, stat.st_dev)
    return realpath, stat_key
