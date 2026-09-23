    def close(self):
        """Close all opened transports."""
        if self._closed:
            return

        self._closed = True

        try:
            if self._loop.is_closed():
                return noop()

            # cancel cleanup task
            if self._cleanup_handle:
                self._cleanup_handle.cancel()

            # cancel cleanup close task
            if self._cleanup_closed_handle:
                self._cleanup_closed_handle.cancel()

            for data in self._conns.values():
                for proto, t0 in data:
                    proto.close()

            for proto in self._acquired:
                proto.close()

            for transport in self._cleanup_closed_transports:
                if transport is not None:
                    transport.abort()

        finally:
            self._conns.clear()
            self._acquired.clear()
            self._waiters.clear()
            self._cleanup_handle = None
            self._cleanup_closed_transports.clear()
            self._cleanup_closed_handle = None
