    def __getstate__(self):
        d = self.__dict__.copy()
        d['stale_callback'] = None
        return d
