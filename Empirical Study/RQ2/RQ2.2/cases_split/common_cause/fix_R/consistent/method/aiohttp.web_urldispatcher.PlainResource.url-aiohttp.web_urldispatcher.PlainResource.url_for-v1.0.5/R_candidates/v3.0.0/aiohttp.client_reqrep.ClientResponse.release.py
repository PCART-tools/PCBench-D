    def release(self):
        if self._closed:
            return noop()

        self._closed = True
        if self._connection is not None:
            self._connection.release()
            self._connection = None

        self._cleanup_writer()
        self._notify_content()
        return noop()
