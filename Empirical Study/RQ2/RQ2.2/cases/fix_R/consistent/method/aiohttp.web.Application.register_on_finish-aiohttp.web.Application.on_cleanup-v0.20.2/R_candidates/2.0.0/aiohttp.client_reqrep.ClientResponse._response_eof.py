    def _response_eof(self):
        if self._closed:
            return

        if self._connection is not None:
            # websocket
            if self._connection.protocol.upgraded:
                return

            self._connection.release()
            self._connection = None

        self._closed = True
        self._cleanup_writer()
