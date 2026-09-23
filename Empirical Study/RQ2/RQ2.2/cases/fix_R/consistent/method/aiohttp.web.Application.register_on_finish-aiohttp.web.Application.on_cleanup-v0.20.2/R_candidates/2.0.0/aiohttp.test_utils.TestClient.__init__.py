    def __init__(self, app_or_server, *, scheme=sentinel, host=sentinel,
                 cookie_jar=None, server_kwargs=None, loop=None, **kwargs):
        if isinstance(app_or_server, BaseTestServer):
            if scheme is not sentinel or host is not sentinel:
                raise ValueError("scheme and host are mutable exclusive "
                                 "with TestServer parameter")
            self._server = app_or_server
        elif isinstance(app_or_server, Application):
            scheme = "http" if scheme is sentinel else scheme
            host = '127.0.0.1' if host is sentinel else host
            server_kwargs = server_kwargs or {}
            self._server = TestServer(
                app_or_server,
                scheme=scheme, host=host, **server_kwargs)
        else:
            raise TypeError("app_or_server should be either web.Application "
                            "or TestServer instance")
        self._loop = loop
        if cookie_jar is None:
            cookie_jar = aiohttp.CookieJar(unsafe=True, loop=loop)
        self._session = ClientSession(loop=loop,
                                      cookie_jar=cookie_jar,
                                      **kwargs)
        self._closed = False
        self._responses = []
        self._websockets = []
