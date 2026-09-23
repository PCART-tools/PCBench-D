    @asyncio.coroutine
    def resolve(self, host, port=0, family=socket.AF_INET):
        hosts = []
        resp = yield from self._resolver.gethostbyname(host, family)

        for address in resp.addresses:
            hosts.append(
                {'hostname': host,
                 'host': address, 'port': port,
                 'family': family, 'proto': 0,
                 'flags': socket.AI_NUMERICHOST})
        return hosts
