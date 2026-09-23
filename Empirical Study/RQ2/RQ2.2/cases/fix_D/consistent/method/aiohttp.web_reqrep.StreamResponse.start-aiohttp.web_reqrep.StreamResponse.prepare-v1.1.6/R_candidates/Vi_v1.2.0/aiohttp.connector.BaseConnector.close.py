    def close(self):
        """Close all opened transports."""
        ret = helpers.create_future(self._loop)
        ret.set_result(None)
        if self._closed:
            return ret
        self._closed = True

        try:
            if self._loop.is_closed():
                return ret

            for key, data in self._conns.items():
                for transport, proto, t0 in data:
                    transport.close()

            for transport in chain(*self._acquired.values()):
                transport.close()

            if self._cleanup_handle:
                self._cleanup_handle.cancel()

        finally:
            self._conns.clear()
            self._acquired.clear()
            self._cleanup_handle = None
        return ret
