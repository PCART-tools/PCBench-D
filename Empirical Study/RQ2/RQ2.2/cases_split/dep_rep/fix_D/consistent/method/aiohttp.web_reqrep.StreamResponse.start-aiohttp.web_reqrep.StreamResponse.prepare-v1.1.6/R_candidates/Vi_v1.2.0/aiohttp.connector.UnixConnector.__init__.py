    def __init__(self, path, force_close=False, conn_timeout=None,
                 keepalive_timeout=sentinel, limit=20, loop=None):
        super().__init__(force_close=force_close,
                         conn_timeout=conn_timeout,
                         keepalive_timeout=keepalive_timeout,
                         limit=limit, loop=loop)
        self._path = path
