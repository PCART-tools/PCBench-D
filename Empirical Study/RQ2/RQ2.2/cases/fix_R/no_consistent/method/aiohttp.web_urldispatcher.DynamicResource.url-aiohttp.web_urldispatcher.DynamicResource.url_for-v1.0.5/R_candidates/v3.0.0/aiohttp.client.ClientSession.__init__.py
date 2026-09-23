    def __init__(self, *, connector=None, loop=None, cookies=None,
                 headers=None, skip_auto_headers=None,
                 auth=None, json_serialize=json.dumps,
                 request_class=ClientRequest, response_class=ClientResponse,
                 ws_response_class=ClientWebSocketResponse,
                 version=http.HttpVersion11,
                 cookie_jar=None, connector_owner=True, raise_for_status=False,
                 read_timeout=sentinel, conn_timeout=None,
                 auto_decompress=True, trust_env=False,
                 trace_configs=None):

        implicit_loop = False
        if loop is None:
            if connector is not None:
                loop = connector._loop
            else:
                implicit_loop = True
                loop = asyncio.get_event_loop()

        if connector is None:
            connector = TCPConnector(loop=loop)

        if connector._loop is not loop:
            raise RuntimeError(
                "Session and connector has to use same event loop")

        self._loop = loop

        if loop.get_debug():
            self._source_traceback = traceback.extract_stack(sys._getframe(1))

        if implicit_loop and not loop.is_running():
            warnings.warn("Creating a client session outside of coroutine is "
                          "a very dangerous idea",
                          stacklevel=2)
            context = {'client_session': self,
                       'message': 'Creating a client session outside '
                       'of coroutine'}
            if self._source_traceback is not None:
                context['source_traceback'] = self._source_traceback
            loop.call_exception_handler(context)

        if cookie_jar is None:
            cookie_jar = CookieJar(loop=loop)
        self._cookie_jar = cookie_jar

        if cookies is not None:
            self._cookie_jar.update_cookies(cookies)

        self._connector = connector
        self._connector_owner = connector_owner
        self._default_auth = auth
        self._version = version
        self._json_serialize = json_serialize
        self._read_timeout = (read_timeout if read_timeout is not sentinel
                              else DEFAULT_TIMEOUT)
        self._conn_timeout = conn_timeout
        self._raise_for_status = raise_for_status
        self._auto_decompress = auto_decompress
        self._trust_env = trust_env

        # Convert to list of tuples
        if headers:
            headers = CIMultiDict(headers)
        else:
            headers = CIMultiDict()
        self._default_headers = headers
        if skip_auto_headers is not None:
            self._skip_auto_headers = frozenset([istr(i)
                                                 for i in skip_auto_headers])
        else:
            self._skip_auto_headers = frozenset()

        self._request_class = request_class
        self._response_class = response_class
        self._ws_response_class = ws_response_class

        self._trace_configs = trace_configs or []
        for trace_config in self._trace_configs:
            trace_config.freeze()
