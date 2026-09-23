    @asyncio.coroutine
    def _create_proxy_connection(self, req):
        headers = {}
        if req.proxy_headers is not None:
            headers = req.proxy_headers
        headers[hdrs.HOST] = req.headers[hdrs.HOST]

        proxy_req = ClientRequest(
            hdrs.METH_GET, req.proxy,
            headers=headers,
            auth=req.proxy_auth,
            loop=self._loop,
            verify_ssl=req.verify_ssl,
            fingerprint=req.fingerprint,
            ssl_context=req.ssl_context)

        # create connection to proxy server
        transport, proto = yield from self._create_direct_connection(
            proxy_req, client_error=ClientProxyConnectionError)

        auth = proxy_req.headers.pop(hdrs.AUTHORIZATION, None)
        if auth is not None:
            if not req.ssl:
                req.headers[hdrs.PROXY_AUTHORIZATION] = auth
            else:
                proxy_req.headers[hdrs.PROXY_AUTHORIZATION] = auth

        if req.ssl:
            sslcontext = self._get_ssl_context(req)
            # For HTTPS requests over HTTP proxy
            # we must notify proxy to tunnel connection
            # so we send CONNECT command:
            #   CONNECT www.python.org:443 HTTP/1.1
            #   Host: www.python.org
            #
            # next we must do TLS handshake and so on
            # to do this we must wrap raw socket into secure one
            # asyncio handles this perfectly
            proxy_req.method = hdrs.METH_CONNECT
            proxy_req.url = req.url
            key = (req.host, req.port, req.ssl)
            conn = Connection(self, key, proto, self._loop)
            proxy_resp = proxy_req.send(conn)
            try:
                resp = yield from proxy_resp.start(conn, True)
            except:
                proxy_resp.close()
                conn.close()
                raise
            else:
                conn._protocol = None
                conn._transport = None
                try:
                    if resp.status != 200:
                        raise ClientHttpProxyError(
                            proxy_resp.request_info,
                            resp.history,
                            code=resp.status,
                            message=resp.reason,
                            headers=resp.headers)
                    rawsock = transport.get_extra_info('socket', default=None)
                    if rawsock is None:
                        raise RuntimeError(
                            "Transport does not expose socket instance")
                    # Duplicate the socket, so now we can close proxy transport
                    rawsock = rawsock.dup()
                finally:
                    transport.close()

                transport, proto = yield from self._wrap_create_connection(
                    self._factory, ssl=sslcontext, sock=rawsock,
                    server_hostname=req.host,
                    req=req)
            finally:
                proxy_resp.close()

        return transport, proto
