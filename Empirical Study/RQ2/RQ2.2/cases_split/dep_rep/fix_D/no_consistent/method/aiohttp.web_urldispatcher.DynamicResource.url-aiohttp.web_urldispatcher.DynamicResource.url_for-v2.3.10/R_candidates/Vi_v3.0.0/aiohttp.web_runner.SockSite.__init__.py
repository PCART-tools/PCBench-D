    def __init__(self, runner, sock, *,
                 shutdown_timeout=60.0, ssl_context=None,
                 backlog=128):
        super().__init__(runner, shutdown_timeout=shutdown_timeout,
                         ssl_context=ssl_context, backlog=backlog)
        self._sock = sock
        scheme = 'https' if self._ssl_context else 'http'
        if hasattr(socket, 'AF_UNIX') and sock.family == socket.AF_UNIX:
            name = '{}://unix:{}:'.format(scheme, sock.getsockname())
        else:
            host, port = sock.getsockname()[:2]
            name = str(URL.build(scheme=scheme, host=host, port=port))
        self._name = name
