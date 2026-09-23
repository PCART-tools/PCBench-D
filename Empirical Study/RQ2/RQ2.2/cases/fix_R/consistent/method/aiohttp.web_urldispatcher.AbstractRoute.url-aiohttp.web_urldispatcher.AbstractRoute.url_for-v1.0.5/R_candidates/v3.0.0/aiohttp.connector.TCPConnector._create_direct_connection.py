    async def _create_direct_connection(self, req,
                                        *, client_error=ClientConnectorError,
                                        traces=None):
        sslcontext = self._get_ssl_context(req)
        fingerprint = self._get_fingerprint(req)

        try:
            hosts = await self._resolve_host(
                req.url.raw_host,
                req.port,
                traces=traces)
        except OSError as exc:
            # in case of proxy it is not ClientProxyConnectionError
            # it is problem of resolving proxy ip itself
            raise ClientConnectorError(req.connection_key, exc) from exc

        last_exc = None

        for hinfo in hosts:
            host = hinfo['host']
            port = hinfo['port']

            try:
                transp, proto = await self._wrap_create_connection(
                    self._factory, host, port,
                    ssl=sslcontext, family=hinfo['family'],
                    proto=hinfo['proto'], flags=hinfo['flags'],
                    server_hostname=hinfo['hostname'] if sslcontext else None,
                    local_addr=self._local_addr,
                    req=req, client_error=client_error)
            except ClientConnectorError as exc:
                last_exc = exc
                continue

            if req.is_ssl() and fingerprint:
                try:
                    fingerprint.check(transp)
                except ServerFingerprintMismatch as exc:
                    transp.close()
                    if not self._cleanup_closed_disabled:
                        self._cleanup_closed_transports.append(transp)
                    last_exc = exc
                    continue

            return transp, proto
        else:
            raise last_exc
