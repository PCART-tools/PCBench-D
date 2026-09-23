    @asyncio.coroutine
    def resolve_with_query(self, host, port=0, family=socket.AF_INET):
        if family == socket.AF_INET6:
            qtype = 'AAAA'
        else:
            qtype = 'A'

        hosts = []
        resp = yield from self._resolver.query(host, qtype)

        for rr in resp:
            hosts.append(
                {'hostname': host,
                 'host': rr.host, 'port': port,
                 'family': family, 'proto': 0,
                 'flags': socket.AI_NUMERICHOST})

        return hosts
