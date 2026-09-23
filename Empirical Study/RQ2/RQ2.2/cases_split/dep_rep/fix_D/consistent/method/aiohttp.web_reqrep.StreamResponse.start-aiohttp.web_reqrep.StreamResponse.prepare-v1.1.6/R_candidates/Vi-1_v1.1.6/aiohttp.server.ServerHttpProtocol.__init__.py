    def __init__(self, *, loop=None,
                 keepalive_timeout=75,  # NGINX default value is 75 secs
                 tcp_keepalive=True,
                 slow_request_timeout=0,
                 logger=server_logger,
                 access_log=access_logger,
                 access_log_format=helpers.AccessLogger.LOG_FORMAT,
                 debug=False,
                 max_line_size=8190,
                 max_headers=32768,
                 max_field_size=8190,
                 **kwargs):

        # process deprecated params
        logger = _get_kwarg(kwargs, 'log', 'logger', logger)

        tcp_keepalive = _get_kwarg(kwargs, 'keep_alive_on',
                                   'tcp_keepalive', tcp_keepalive)

        keepalive_timeout = _get_kwarg(kwargs, 'keep_alive',
                                       'keepalive_timeout', keepalive_timeout)

        slow_request_timeout = _get_kwarg(kwargs, 'timeout',
                                          'slow_request_timeout',
                                          slow_request_timeout)

        super().__init__(
            loop=loop,
            disconnect_error=errors.ClientDisconnectedError, **kwargs)

        self._tcp_keepalive = tcp_keepalive
        self._keepalive_timeout = keepalive_timeout
        self._slow_request_timeout = slow_request_timeout
        self._loop = loop if loop is not None else asyncio.get_event_loop()

        self._request_prefix = aiohttp.HttpPrefixParser()
        self._request_parser = aiohttp.HttpRequestParser(
            max_line_size=max_line_size,
            max_field_size=max_field_size,
            max_headers=max_headers)

        self.logger = logger
        self.debug = debug
        self.access_log = access_log
        if access_log:
            self.access_logger = helpers.AccessLogger(access_log,
                                                      access_log_format)
        else:
            self.access_logger = None
        self._closing = False
