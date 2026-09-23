    def __init__(self, *, loop=None):
        asyncio.streams.FlowControlMixin.__init__(self, loop=loop)
        DataQueue.__init__(self, loop=loop)

        self.transport = None
        self._should_close = False

        self._message = None
        self._payload = None
        self._skip_payload = False
        self._payload_parser = None
        self._reading_paused = False

        self._timer = None

        self._tail = b''
        self._upgraded = False
        self._parser = None
