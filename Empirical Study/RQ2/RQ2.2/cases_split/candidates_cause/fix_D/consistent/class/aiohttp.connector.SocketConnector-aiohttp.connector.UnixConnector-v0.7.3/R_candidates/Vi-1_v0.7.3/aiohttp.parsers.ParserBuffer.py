class ParserBuffer(bytearray):
    """ParserBuffer is a bytearray extension.

    ParserBuffer provides helper methods for parsers.
    """

    def __init__(self, *args, limit=BUF_LIMIT):
        super().__init__(*args)

        self.offset = 0
        self.size = 0
        self._limit = limit
        self._exception = None
        self._writer = self._feed_data()
        next(self._writer)

    def exception(self):
        return self._exception

    def set_exception(self, exc):
        self._exception = exc

    def shrink(self):
        if self.offset:
            del self[:self.offset]
            self.offset = 0
            self.size = len(self)

    def _feed_data(self):
        while True:
            chunk = yield
            if chunk:
                chunk_len = len(chunk)
                self.size += chunk_len
                self.extend(chunk)

            # shrink buffer
            if (self.offset and len(self) > self._limit):
                self.shrink()

            if self._exception:
                self._writer = self._feed_data()
                next(self._writer)
                raise self._exception

    def feed_data(self, data):
        self._writer.send(data)

    def read(self, size):
        """read() reads specified amount of bytes."""

        while True:
            if self.size >= size:
                start, end = self.offset, self.offset + size
                self.offset = end
                self.size = self.size - size
                return self[start:end]

            self._writer.send((yield))

    def readsome(self, size=None):
        """reads size of less amount of bytes."""

        while True:
            if self.size > 0:
                if size is None or self.size < size:
                    size = self.size

                start, end = self.offset, self.offset + size
                self.offset = end
                self.size = self.size - size

                return self[start:end]

            self._writer.send((yield))

    def readuntil(self, stop, limit=None, exc=ValueError):
        assert isinstance(stop, bytes) and stop, \
            'bytes is required: {!r}'.format(stop)

        stop_len = len(stop)

        while True:
            pos = self.find(stop, self.offset)
            if pos >= 0:
                end = pos + stop_len
                size = end - self.offset
                if limit is not None and size > limit:
                    raise exc('Line is too long.')

                start, self.offset = self.offset, end
                self.size = self.size - size

                return self[start:end]
            else:
                if limit is not None and self.size > limit:
                    raise exc('Line is too long.')

            self._writer.send((yield))

    def wait(self, size):
        """wait() waits for specified amount of bytes
        then returns data without changing internal buffer."""

        while True:
            if self.size >= size:
                return self[self.offset:self.offset + size]

            self._writer.send((yield))

    def waituntil(self, stop, limit=None, exc=ValueError):
        """waituntil() reads until `stop` bytes sequence."""
        assert isinstance(stop, bytes) and stop, \
            'bytes is required: {!r}'.format(stop)

        stop_len = len(stop)

        while True:
            pos = self.find(stop, self.offset)
            if pos >= 0:
                end = pos + stop_len
                size = end - self.offset
                if limit is not None and size > limit:
                    raise exc('Line is too long. %s' % bytes(self))

                return self[self.offset:end]
            else:
                if limit is not None and self.size > limit:
                    raise exc('Line is too long. %s' % bytes(self))

            self._writer.send((yield))

    def skip(self, size):
        """skip() skips specified amount of bytes."""

        while self.size < size:
            self._writer.send((yield))

        self.size -= size
        self.offset += size

    def skipuntil(self, stop):
        """skipuntil() reads until `stop` bytes sequence."""
        assert isinstance(stop, bytes) and stop, \
            'bytes is required: {!r}'.format(stop)

        stop_len = len(stop)

        while True:
            stop_line = self.find(stop, self.offset)
            if stop_line >= 0:
                end = stop_line + stop_len
                self.size = self.size - (end - self.offset)
                self.offset = end
                return
            else:
                self.size = 0
                self.offset = len(self) - 1

            self._writer.send((yield))

    def __bytes__(self):
        return bytes(self[self.offset:])
