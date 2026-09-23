    @asyncio.coroutine
    def connect(self, req):
        """Get from pool or create new connection."""
        key = req.connection_key

        if self._limit:
            # total calc available connections
            available = self._limit - len(self._acquired)

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
            try:
                yield from fut
            finally:
                # remove a waiter even if it was cancelled
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
                if self._closed:
                    proto.close()
                    raise ClientConnectionError("Connector is closed.")
            except:
                # signal to waiter
                if key in self._waiters:
                    for waiter in self._waiters[key]:
                        if not waiter.done():
                            waiter.set_result(None)
                            break
                raise
            finally:
                if not self._closed:
                    self._acquired.remove(placeholder)
                    self._drop_acquired_per_host(key, placeholder)

        self._acquired.add(proto)
        self._acquired_per_host[key].add(proto)
        return Connection(self, key, proto, self._loop)
