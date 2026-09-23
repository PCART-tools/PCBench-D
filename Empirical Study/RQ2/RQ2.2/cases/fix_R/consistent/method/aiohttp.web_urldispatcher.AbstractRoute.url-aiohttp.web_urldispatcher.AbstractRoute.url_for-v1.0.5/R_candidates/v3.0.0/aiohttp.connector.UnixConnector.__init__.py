    def __init__(self, path, force_close=False, keepalive_timeout=sentinel,
                 limit=100, limit_per_host=0, loop=None):
        super().__init__(force_close=force_close,
                         keepalive_timeout=keepalive_timeout,
                         limit=limit, limit_per_host=limit_per_host, loop=loop)
        self._path = path
