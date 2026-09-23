    @asyncio.coroutine
    def _create_direct_connection(self, req):
        if req.ssl:
            sslcontext = self.ssl_context
        else:
            sslcontext = None

        hosts = yield from self._resolve_host(req.host, req.port)
        exc = None

        for hinfo in hosts:
            try:
                host = hinfo['host']
                port = hinfo['port']
                transp, proto = yield from self._loop.create_connection(
                    self._factory, host, port,
                    ssl=sslcontext, family=hinfo['family'],
                    proto=hinfo['proto'], flags=hinfo['flags'],
                    server_hostname=hinfo['hostname'] if sslcontext else None,
                    local_addr=self._local_addr)
                has_cert = transp.get_extra_info('sslcontext')
                if has_cert and self._fingerprint:
                    sock = transp.get_extra_info('socket')
                    if not hasattr(sock, 'getpeercert'):
                        # Workaround for asyncio 3.5.0
                        # Starting from 3.5.1 version
                        # there is 'ssl_object' extra info in transport
                        sock = transp._ssl_protocol._sslpipe.ssl_object
                    # gives DER-encoded cert as a sequence of bytes (or None)
                    cert = sock.getpeercert(binary_form=True)
                    assert cert
                    got = self._hashfunc(cert).digest()
                    expected = self._fingerprint
                    if got != expected:
                        transp.close()
                        raise FingerprintMismatch(expected, got, host, port)
                return transp, proto
            except OSError as e:
                exc = e
        else:
            raise ClientOSError(exc.errno,
                                'Can not connect to %s:%s [%s]' %
                                (req.host, req.port, exc.strerror)) from exc
