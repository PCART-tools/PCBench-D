class BaseConnector(object):

    def __init__(self, *, conn_timeout=None, keepalive_timeout=30,
                 share_cookies=False, force_close=False, loop=None, **kwargs):
        self._conns = {}
        self._conn_timeout = conn_timeout
        self._keepalive_timeout = keepalive_timeout
        self._share_cookies = share_cookies
        self._cleanup_handle = None
        self._force_close = force_close

        if loop is None:
            loop = asyncio.get_event_loop()
        self._loop = loop
        self._factory = functools.partial(aiohttp.StreamProtocol, loop=loop)

        self.cookies = http.cookies.SimpleCookie()
        self._wr = weakref.ref(
            self, lambda wr, f=self._do_close, conns=self._conns: f(conns))

    def _cleanup(self):
        """Cleanup unused transports."""
        if self._cleanup_handle:
            self._cleanup_handle.cancel()
            self._cleanup_handle = None

        now = time.time()

        connections = {}
        for key, conns in self._conns.items():
            alive = []
            for transport, proto, t0 in conns:
                if transport is not None:
                    if proto and not proto.is_connected():
                        transport = None
                    elif (now - t0) > self._keepalive_timeout:
                        transport.close()
                        transport = None

                if transport:
                    alive.append((transport, proto, t0))
            if alive:
                connections[key] = alive

        if connections:
            self._cleanup_handle = self._loop.call_later(
                self._keepalive_timeout, self._cleanup)

        self._conns = connections
        self._wr = weakref.ref(
            self, lambda wr, f=self._do_close, conns=self._conns: f(conns))

    def _start_cleanup_task(self):
        if self._cleanup_handle is None:
            self._cleanup_handle = self._loop.call_later(
                self._keepalive_timeout, self._cleanup)

    def close(self):
        """Close all opened transports."""
        self._do_close(self._conns)

    @staticmethod
    def _do_close(conns):
        for key, data in conns.items():
            for transport, proto, td in data:
                transport.close()

        conns.clear()

    def update_cookies(self, cookies):
        if isinstance(cookies, dict):
            cookies = cookies.items()

        for name, value in cookies:
            if isinstance(value, http.cookies.Morsel):
                # use dict method because SimpleCookie class modifies value
                dict.__setitem__(self.cookies, name, value)
            else:
                self.cookies[name] = value

    @asyncio.coroutine
    def connect(self, req):
        key = (req.host, req.port, req.ssl)

        if self._share_cookies:
            req.update_cookies(self.cookies.items())

        transport, proto = self._get(key)
        if transport is None:
            if self._conn_timeout:
                transport, proto = yield from asyncio.wait_for(
                    self._create_connection(req),
                    self._conn_timeout, loop=self._loop)
            else:
                transport, proto = yield from self._create_connection(req)

        return Connection(self, key, req, transport, proto)

    def _get(self, key):
        conns = self._conns.get(key)
        while conns:
            transport, proto, t0 = conns.pop()
            if transport is not None and proto.is_connected():
                if (time.time() - t0) > self._keepalive_timeout:
                    transport.close()
                    transport = None
                else:
                    return transport, proto

        return None, None

    def _release(self, key, req, transport, protocol):
        resp = req.response
        should_close = False

        if resp is not None:
            if resp.message is None:
                should_close = True
            else:
                should_close = resp.message.should_close
                if self._share_cookies and resp.cookies:
                    self.update_cookies(resp.cookies.items())

        if self._force_close:
            should_close = True

        reader = protocol.reader
        if should_close or (reader.output and not reader.output.at_eof()):
            transport.close()
        else:
            conns = self._conns.get(key)
            if conns is None:
                conns = self._conns[key] = []
            conns.append((transport, protocol, time.time()))
            reader.unset_parser()

            self._start_cleanup_task()

    def _create_connection(self, req, *args, **kwargs):
        raise NotImplementedError()
