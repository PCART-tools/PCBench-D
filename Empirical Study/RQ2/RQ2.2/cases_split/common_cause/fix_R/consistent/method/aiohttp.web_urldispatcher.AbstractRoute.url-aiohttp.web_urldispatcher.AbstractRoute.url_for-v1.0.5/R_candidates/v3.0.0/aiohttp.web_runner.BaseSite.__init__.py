    def __init__(self, runner, *,
                 shutdown_timeout=60.0, ssl_context=None,
                 backlog=128):
        if runner.server is None:
            raise RuntimeError("Call runner.setup() before making a site")
        self._runner = runner
        self._shutdown_timeout = shutdown_timeout
        self._ssl_context = ssl_context
        self._backlog = backlog
        self._server = None
