    def __init__(self, *, loop=None, **kwargs):
        asyncio.streams.FlowControlMixin.__init__(self, loop=loop)
        DataQueue.__init__(self, loop=loop)

        self.paused = False
        self.transport = None
        self.writer = None
        self._should_close = False

        self._message = None
        self._payload = None
        self._payload_parser = None
        self._reading_paused = False

        self._timer = None
        self._skip_status = ()

        self._tail = b''
        self._upgraded = False
        self._parser = None
