    def __init__(self, app, router, *,
                 handler=RequestHandler, loop=None,
                 secure_proxy_ssl_header=None, **kwargs):
        self._app = app
        self._router = router
        self._handler = handler
        self._loop = loop
        self._connections = {}
        self._secure_proxy_ssl_header = secure_proxy_ssl_header
        self._kwargs = kwargs
        self._kwargs.setdefault('logger', app.logger)
        self._requests_count = 0
        self._time_service = TimeService(self._loop)
