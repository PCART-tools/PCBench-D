    def _release(self, key, protocol, *, should_close=False):
        if self._closed:
            # acquired connection is already released on connector closing
            return

        self._release_acquired(key, protocol)

        if self._force_close:
            should_close = True

        if should_close or protocol.should_close:
            transport = protocol.close()

            if key[-1] and not self._cleanup_closed_disabled:
                self._cleanup_closed_transports.append(transport)
        else:
            conns = self._conns.get(key)
            if conns is None:
                conns = self._conns[key] = []
            conns.append((protocol, self._loop.time()))

            if self._cleanup_handle is None:
                self._cleanup_handle = helpers.weakref_handle(
                    self._cleanup, self._keepalive_timeout, self._loop)
