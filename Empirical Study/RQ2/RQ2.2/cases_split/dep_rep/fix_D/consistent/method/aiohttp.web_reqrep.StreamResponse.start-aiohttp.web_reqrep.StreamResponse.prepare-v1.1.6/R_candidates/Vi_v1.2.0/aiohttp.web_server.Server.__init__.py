    def __init__(self, handler, *, request_factory=None, loop=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        self._handler = handler
        self._request_factory = request_factory or self._make_request
        self._loop = loop
        self._connections = {}
        self._kwargs = kwargs
        self._requests_count = 0
        self._time_service = TimeService(self._loop)
