    def _response_eof(self):
        if self._closed:
            return

        if self._connection is not None:
            # websocket, protocol could be None because
            # connection could be detached
            if (self._connection.protocol is not None and
                    self._connection.protocol.upgraded):
                return

            self._connection.release()
            self._connection = None

        self._closed = True
        self._cleanup_writer()
