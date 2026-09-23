    @asyncio.coroutine
    def _resolve_with_query(self, host, port=0, family=socket.AF_INET):
        if family == socket.AF_INET6:
            qtype = 'AAAA'
        else:
            qtype = 'A'

        try:
            resp = yield from self._resolver.query(host, qtype)
        except aiodns.error.DNSError as exc:
            msg = exc.args[1] if len(exc.args) >= 1 else "DNS lookup failed"
            raise OSError(msg) from exc

        hosts = []
        for rr in resp:
            hosts.append(
                {'hostname': host,
                 'host': rr.host, 'port': port,
                 'family': family, 'proto': 0,
                 'flags': socket.AI_NUMERICHOST})

        if not hosts:
            raise OSError("DNS lookup failed")

        return hosts
