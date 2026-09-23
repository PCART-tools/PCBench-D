    def __init__(self, server, *, cookie_jar=None, loop=None, **kwargs):
        if not isinstance(server, BaseTestServer):
            raise TypeError("server must be web.Application TestServer "
                            "instance, found type: %r" % type(server))
        self._server = server
        self._loop = loop
        if cookie_jar is None:
            cookie_jar = aiohttp.CookieJar(unsafe=True, loop=loop)
        self._session = ClientSession(loop=loop,
                                      cookie_jar=cookie_jar,
                                      **kwargs)
        self._closed = False
        self._responses = []
        self._websockets = []
