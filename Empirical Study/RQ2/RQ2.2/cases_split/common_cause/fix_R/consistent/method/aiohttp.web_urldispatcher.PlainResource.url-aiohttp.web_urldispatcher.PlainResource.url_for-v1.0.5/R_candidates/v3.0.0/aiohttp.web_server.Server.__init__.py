    def __init__(self, handler, *, request_factory=None, loop=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        self._loop = loop
        self._connections = {}
        self._kwargs = kwargs
        self.requests_count = 0
        self.request_handler = handler
        self.request_factory = request_factory or self._make_request
