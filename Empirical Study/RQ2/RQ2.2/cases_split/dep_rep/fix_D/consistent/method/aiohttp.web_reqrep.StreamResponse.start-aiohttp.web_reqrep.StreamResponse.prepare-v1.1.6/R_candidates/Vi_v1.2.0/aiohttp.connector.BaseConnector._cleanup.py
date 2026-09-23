    def _cleanup(self):
        """Cleanup unused transports."""
        if self._cleanup_handle:
            self._cleanup_handle.cancel()
            self._cleanup_handle = None

        now = self._loop.time()

        connections = {}
        timeout = self._keepalive_timeout

        for key, conns in self._conns.items():
            alive = []
            for transport, proto, t0 in conns:
                if transport is not None:
                    if proto and not proto.is_connected():
                        transport = None
                    else:
                        delta = t0 + self._keepalive_timeout - now
                        if delta < 0:
                            transport.close()
                            transport = None
                        elif delta < timeout:
                            timeout = delta

                if transport is not None:
                    alive.append((transport, proto, t0))
            if alive:
                connections[key] = alive

        if connections:
            self._cleanup_handle = self._loop.call_at(
                ceil(now + timeout), self._cleanup)

        self._conns = connections
