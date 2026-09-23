    @asyncio.coroutine
    def connect(self, req):
        """Get from pool or create new connection."""
        key = (req.host, req.port, req.ssl)

        if self._limit:
            # total calc available connections
            available = self._limit - len(self._waiters) - len(self._acquired)

            # check limit per host
            if (self._limit_per_host and available > 0 and
                    key in self._acquired_per_host):
                available = self._limit_per_host - len(
                    self._acquired_per_host.get(key))

        elif self._limit_per_host and key in self._acquired_per_host:
            # check limit per host
            available = self._limit_per_host - len(
                self._acquired_per_host.get(key))
        else:
            available = 1

        # Wait if there are no available connections.
        if available <= 0:
            fut = helpers.create_future(self._loop)

            # This connection will now count towards the limit.
            waiters = self._waiters[key]
            waiters.append(fut)
            yield from fut
            waiters.remove(fut)
            if not waiters:
                del self._waiters[key]

        proto = self._get(key)
        if proto is None:
            placeholder = _TransportPlaceholder()
            self._acquired.add(placeholder)
            self._acquired_per_host[key].add(placeholder)
            try:
                proto = yield from self._create_connection(req)
            except OSError as exc:
                raise ClientConnectorError(
                    exc.errno,
                    'Cannot connect to host {0[0]}:{0[1]} ssl:{0[2]} [{1}]'
                    .format(key, exc.strerror)) from exc
            finally:
                self._acquired.remove(placeholder)
                self._acquired_per_host[key].remove(placeholder)

        self._acquired.add(proto)
        self._acquired_per_host[key].add(proto)
        return Connection(self, key, proto, self._loop)
