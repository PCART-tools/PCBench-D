    def close(self):
        if self._closed:
            return

        self._closed = True
        if self._loop is None or self._loop.is_closed():
            return

        if self._connection is not None:
            self._connection.close()
            self._connection = None
        self._cleanup_writer()
        self._notify_content()
