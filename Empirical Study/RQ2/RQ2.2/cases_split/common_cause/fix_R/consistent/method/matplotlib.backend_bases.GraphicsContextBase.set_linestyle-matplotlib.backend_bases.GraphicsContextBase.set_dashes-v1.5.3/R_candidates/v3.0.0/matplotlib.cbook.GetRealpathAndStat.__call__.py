    def __call__(self, path):
        result = self._cache.get(path)
        if result is None:
            realpath = os.path.realpath(path)
            if sys.platform == 'win32':
                stat_key = realpath
            else:
                stat = os.stat(realpath)
                stat_key = (stat.st_ino, stat.st_dev)
            result = realpath, stat_key
            self._cache[path] = result
        return result
