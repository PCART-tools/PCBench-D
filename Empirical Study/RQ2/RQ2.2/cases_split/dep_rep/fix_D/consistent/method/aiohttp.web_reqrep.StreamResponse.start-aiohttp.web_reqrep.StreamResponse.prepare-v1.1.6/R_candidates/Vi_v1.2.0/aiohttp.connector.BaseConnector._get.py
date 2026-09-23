    def _get(self, key):
        try:
            conns = self._conns[key]
        except KeyError:
            return None, None
        t1 = self._loop.time()
        while conns:
            transport, proto, t0 = conns.pop()
            if transport is not None and proto.is_connected():
                if t1 - t0 > self._keepalive_timeout:
                    transport.close()
                    transport = None
                else:
                    if not conns:
                        # The very last connection was reclaimed: drop the key
                        del self._conns[key]
                    return transport, proto
        # No more connections: drop the key
        del self._conns[key]
        return None, None
