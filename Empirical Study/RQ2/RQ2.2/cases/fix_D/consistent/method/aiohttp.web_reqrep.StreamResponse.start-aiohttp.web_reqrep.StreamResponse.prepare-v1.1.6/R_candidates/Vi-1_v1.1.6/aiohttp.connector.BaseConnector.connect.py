    @asyncio.coroutine
    def connect(self, req):
        """Get from pool or create new connection."""
        key = (req.host, req.port, req.ssl)

        limit = self._limit
        if limit is not None:
            fut = helpers.create_future(self._loop)
            waiters = self._waiters[key]

            # The limit defines the maximum number of concurrent connections
            # for a key. Waiters must be counted against the limit, even before
            # the underlying connection is created.
            available = limit - len(waiters) - len(self._acquired[key])

            # Don't wait if there are connections available.
            if available > 0:
                fut.set_result(None)

            # This connection will now count towards the limit.
            waiters.append(fut)

        try:
            if limit is not None:
                yield from fut

            transport, proto = self._get(key)
            if transport is None:
                try:
                    if self._conn_timeout:
                        transport, proto = yield from asyncio.wait_for(
                            self._create_connection(req),
                            self._conn_timeout, loop=self._loop)
                    else:
                        transport, proto = \
                            yield from self._create_connection(req)

                except asyncio.TimeoutError as exc:
                    raise ClientTimeoutError(
                        'Connection timeout to host {0[0]}:{0[1]} ssl:{0[2]}'
                        .format(key)) from exc
                except OSError as exc:
                    raise ClientOSError(
                        exc.errno,
                        'Cannot connect to host {0[0]}:{0[1]} ssl:{0[2]} [{1}]'
                        .format(key, exc.strerror)) from exc
        except:
            self._release_waiter(key)
            raise

        self._acquired[key].add(transport)
        conn = Connection(self, key, req, transport, proto, self._loop)
        return conn
