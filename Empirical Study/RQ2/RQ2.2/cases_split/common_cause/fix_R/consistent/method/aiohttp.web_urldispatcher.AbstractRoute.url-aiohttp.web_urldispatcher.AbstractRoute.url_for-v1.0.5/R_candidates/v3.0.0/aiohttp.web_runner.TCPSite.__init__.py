    def __init__(self, runner, host=None, port=None, *,
                 shutdown_timeout=60.0, ssl_context=None,
                 backlog=128, reuse_address=None,
                 reuse_port=None):
        super().__init__(runner, shutdown_timeout=shutdown_timeout,
                         ssl_context=ssl_context, backlog=backlog)
        if host is None:
            host = "0.0.0.0"
        self._host = host
        if port is None:
            port = 8443 if self._ssl_context else 8080
        self._port = port
        self._reuse_address = reuse_address
        self._reuse_port = reuse_port
