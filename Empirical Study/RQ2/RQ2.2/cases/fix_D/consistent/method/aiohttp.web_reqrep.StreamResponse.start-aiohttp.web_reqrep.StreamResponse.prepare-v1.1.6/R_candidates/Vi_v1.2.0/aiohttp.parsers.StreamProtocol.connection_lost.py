    def connection_lost(self, exc):
        self.transport = self.writer = None
        self.reader.set_transport(None)

        if exc is None:
            self.reader.feed_eof()
        else:
            self.reader.set_exception(exc)

        super().connection_lost(exc)
