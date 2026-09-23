class UnixConnector(BaseConnector):

    def __init__(self, path, *args, **kw):
        super().__init__(*args, **kw)

        self._path = path

    @property
    def path(self):
        """Path to unix socket"""
        return self._path

    @asyncio.coroutine
    def _create_connection(self, req, **kwargs):
        return (yield from self._loop.create_unix_connection(
            self._factory, self._path, **kwargs))
