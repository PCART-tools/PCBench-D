    @asyncio.coroutine
    def _create_direct_connection(self, req,
                                  *, client_error=ClientConnectorError):
        sslcontext = self._get_ssl_context(req)
        fingerprint, hashfunc = self._get_fingerprint_and_hashfunc(req)

        try:
            hosts = yield from self._resolve_host(req.url.raw_host, req.port)
        except OSError as exc:
            # in case of proxy it is not ClientProxyConnectionError
            # it is problem of resolving proxy ip itself
            raise ClientConnectorError(req.connection_key, exc) from exc

        last_exc = None

        for hinfo in hosts:
            host = hinfo['host']
            port = hinfo['port']

            try:
                transp, proto = yield from self._wrap_create_connection(
                    self._factory, host, port,
                    ssl=sslcontext, family=hinfo['family'],
                    proto=hinfo['proto'], flags=hinfo['flags'],
                    server_hostname=hinfo['hostname'] if sslcontext else None,
                    local_addr=self._local_addr,
                    req=req, client_error=client_error)
            except ClientConnectorError as exc:
                last_exc = exc
                continue

            has_cert = transp.get_extra_info('sslcontext')
            if has_cert and fingerprint:
                sock = transp.get_extra_info('socket')
                if not hasattr(sock, 'getpeercert'):
                    # Workaround for asyncio 3.5.0
                    # Starting from 3.5.1 version
                    # there is 'ssl_object' extra info in transport
                    sock = transp._ssl_protocol._sslpipe.ssl_object
                # gives DER-encoded cert as a sequence of bytes (or None)
                cert = sock.getpeercert(binary_form=True)
                assert cert
                got = hashfunc(cert).digest()
                expected = fingerprint
                if got != expected:
                    transp.close()
                    if not self._cleanup_closed_disabled:
                        self._cleanup_closed_transports.append(transp)
                    last_exc = ServerFingerprintMismatch(
                        expected, got, host, port)
                    continue

            return transp, proto
        else:
            raise last_exc
