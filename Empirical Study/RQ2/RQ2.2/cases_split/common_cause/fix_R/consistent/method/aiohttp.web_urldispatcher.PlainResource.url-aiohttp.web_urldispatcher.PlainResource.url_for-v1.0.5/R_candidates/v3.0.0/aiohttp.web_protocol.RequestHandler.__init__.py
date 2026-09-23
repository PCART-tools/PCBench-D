    def __init__(self, manager, *, loop=None,
                 keepalive_timeout=75,  # NGINX default value is 75 secs
                 tcp_keepalive=True,
                 logger=server_logger,
                 access_log_class=helpers.AccessLogger,
                 access_log=access_logger,
                 access_log_format=helpers.AccessLogger.LOG_FORMAT,
                 debug=False,
                 max_line_size=8190,
                 max_headers=32768,
                 max_field_size=8190,
                 lingering_time=10.0):

        super().__init__(loop=loop)

        self._loop = loop if loop is not None else asyncio.get_event_loop()

        self._manager = manager
        self._request_handler = manager.request_handler
        self._request_factory = manager.request_factory

        self._tcp_keepalive = tcp_keepalive
        self._keepalive_time = None
        self._keepalive_handle = None
        self._keepalive_timeout = keepalive_timeout
        self._lingering_time = float(lingering_time)

        self._messages = deque()
        self._message_tail = b''

        self._waiter = None
        self._error_handler = None
        self._task_handler = self._loop.create_task(self.start())

        self._upgrade = False
        self._payload_parser = None
        self._request_parser = HttpRequestParser(
            self, loop,
            max_line_size=max_line_size,
            max_field_size=max_field_size,
            max_headers=max_headers,
            payload_exception=RequestPayloadError)

        self.transport = None
        self._reading_paused = False

        self.logger = logger
        self.debug = debug
        self.access_log = access_log
        if access_log:
            self.access_logger = access_log_class(
                access_log, access_log_format)
        else:
            self.access_logger = None

        self._close = False
        self._force_close = False
