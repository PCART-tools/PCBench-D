    @asyncio.coroutine
    def resolve(self, host, port=0, family=socket.AF_INET):
        infos = yield from self._loop.getaddrinfo(
            host, port, type=socket.SOCK_STREAM, family=family)

        hosts = []
        for family, _, proto, _, address in infos:
            hosts.append(
                {'hostname': host,
                 'host': address[0], 'port': address[1],
                 'family': family, 'proto': proto,
                 'flags': socket.AI_NUMERICHOST})

        return hosts
