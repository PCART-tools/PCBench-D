    def __init__(self, *, loop=None, disconnect_error=RuntimeError, **kwargs):
        super().__init__(loop=loop)

        self.transport = None
        self.writer = None
        self.reader = StreamParser(
            loop=loop, eof_exc_class=disconnect_error, **kwargs)
