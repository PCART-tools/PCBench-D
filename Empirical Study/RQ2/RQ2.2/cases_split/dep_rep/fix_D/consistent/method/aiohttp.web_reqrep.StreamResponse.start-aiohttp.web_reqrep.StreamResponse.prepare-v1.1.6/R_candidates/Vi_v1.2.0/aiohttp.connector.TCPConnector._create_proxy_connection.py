    @asyncio.coroutine
    def _create_proxy_connection(self, req):
        proxy_req = ClientRequest(
            hdrs.METH_GET, req.proxy,
            headers={hdrs.HOST: req.headers[hdrs.HOST]},
            auth=req.proxy_auth,
            loop=self._loop)
        try:
            # create connection to proxy server
            transport, proto = yield from self._create_direct_connection(
                proxy_req)
        except OSError as exc:
            raise ProxyConnectionError(*exc.args) from exc

        if hdrs.AUTHORIZATION in proxy_req.headers:
            auth = proxy_req.headers[hdrs.AUTHORIZATION]
            del proxy_req.headers[hdrs.AUTHORIZATION]
            if not req.ssl:
                req.headers[hdrs.PROXY_AUTHORIZATION] = auth
            else:
                proxy_req.headers[hdrs.PROXY_AUTHORIZATION] = auth

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
            proxy_req.method = hdrs.METH_CONNECT
            proxy_req.url = req.url
            key = (req.host, req.port, req.ssl)
            conn = Connection(self, key, proxy_req,
                              transport, proto, self._loop)
            self._acquired[key].add(conn._transport)
            proxy_resp = proxy_req.send(conn.writer, conn.reader)
            try:
                resp = yield from proxy_resp.start(conn, True)
            except:
                proxy_resp.close()
                conn.close()
                raise
            else:
                conn.detach()
                try:
                    if resp.status != 200:
                        raise HttpProxyError(code=resp.status,
                                             message=resp.reason)
                    rawsock = transport.get_extra_info('socket', default=None)
                    if rawsock is None:
                        raise RuntimeError(
                            "Transport does not expose socket instance")
                    # Duplicate the socket, so now we can close proxy transport
                    rawsock = rawsock.dup()
                finally:
                    transport.close()

                transport, proto = yield from self._loop.create_connection(
                    self._factory, ssl=self.ssl_context, sock=rawsock,
                    server_hostname=req.host)
            finally:
                proxy_resp.close()

        return transport, proto
