    def __init__(self, handler,
                 *, loop=None, scheme=sentinel, host='127.0.0.1'):
        if loop is None:
            loop = asyncio.get_event_loop()
        self._loop = loop
        self._handler = handler
        super().__init__(scheme=scheme, host=host)
