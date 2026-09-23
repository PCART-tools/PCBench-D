class ProxyConnector(TCPConnector):
    """Http Proxy connector."""

    def __init__(self, proxy, *args, proxy_auth=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._proxy = proxy
        self._proxy_auth = proxy_auth
        assert proxy.startswith('http://'), (
            "Only http proxy supported", proxy)
        assert proxy_auth is None or isinstance(proxy_auth, BasicAuth), (
            "proxy_auth must be None or BasicAuth() tuple", proxy_auth)

    @property
    def proxy(self):
        return self._proxy

    @asyncio.coroutine
    def _create_connection(self, req, **kwargs):
        proxy_req = ClientRequest(
            'GET', self._proxy,
            headers={'Host': req.host},
            auth=self._proxy_auth,
            loop=self._loop)
        try:
            transport, proto = yield from super()._create_connection(proxy_req)
        except OSError as exc:
            raise ProxyConnectionError(*exc.args) from exc
        req.path = '{scheme}://{host}{path}'.format(scheme=req.scheme,
                                                    host=req.host,
                                                    path=req.path)
        if 'AUTHORIZATION' in proxy_req.headers:
            auth = proxy_req.headers['AUTHORIZATION']
            del proxy_req.headers['AUTHORIZATION']
            req.headers['PROXY-AUTHORIZATION'] = auth

        if req.ssl:
            # For HTTPS requests over HTTP proxy
            # we must notify proxy to tunnel connection
            # so we send CONNECT command:
            #   CONNECT www.python.org:443 HTTP/1.1
            #   Host: www.python.org
            #
            # next we must do TLS handshake and so on
            # to do this we must wrap raw socket into secure one
            # asyncio handles this perfectly
            proxy_req.method = 'CONNECT'
            proxy_req.path = '{}:{}'.format(req.host, req.port)
            key = (req.host, req.port, req.ssl)
            conn = Connection(self, key, proxy_req,
                              transport, proto, self._loop)
            proxy_resp = proxy_req.send(conn.writer, conn.reader)
            try:
                resp = yield from proxy_resp.start(conn, True)
            except:
                proxy_resp.close()
                conn.close()
                raise
            else:
                if resp.status != 200:
                    raise HttpProxyError(resp.status, resp.reason)
                rawsock = transport.get_extra_info('socket', default=None)
                if rawsock is None:
                    raise RuntimeError(
                        "Transport does not expose socket instance")
                transport.pause_reading()
                transport, proto = yield from self._loop.create_connection(
                    self._factory, ssl=True, sock=rawsock,
                    server_hostname=req.host, **kwargs)

        return transport, proto
