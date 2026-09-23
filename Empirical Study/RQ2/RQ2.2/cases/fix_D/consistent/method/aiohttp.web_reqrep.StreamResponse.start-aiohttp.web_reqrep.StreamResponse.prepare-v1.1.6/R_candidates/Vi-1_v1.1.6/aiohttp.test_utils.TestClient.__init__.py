    def __init__(self, app_or_server, *, scheme=sentinel, host=sentinel,
                 cookie_jar=None, **kwargs):
        if isinstance(app_or_server, TestServer):
            if scheme is not sentinel or host is not sentinel:
                raise ValueError("scheme and host are mutable exclusive "
                                 "with TestServer parameter")
            self._server = app_or_server
        elif isinstance(app_or_server, Application):
            scheme = "http" if scheme is sentinel else scheme
            host = '127.0.0.1' if host is sentinel else host
            self._server = TestServer(app_or_server,
                                      scheme=scheme, host=host)
        else:
            raise TypeError("app_or_server should be either web.Application "
                            "or TestServer instance")
        self._loop = self._server.app.loop
        if cookie_jar is None:
            cookie_jar = aiohttp.CookieJar(unsafe=True,
                                           loop=self._loop)
        self._session = ClientSession(loop=self._loop,
                                      cookie_jar=cookie_jar,
                                      **kwargs)
        self._closed = False
        self._responses = []
        self._websockets = []
