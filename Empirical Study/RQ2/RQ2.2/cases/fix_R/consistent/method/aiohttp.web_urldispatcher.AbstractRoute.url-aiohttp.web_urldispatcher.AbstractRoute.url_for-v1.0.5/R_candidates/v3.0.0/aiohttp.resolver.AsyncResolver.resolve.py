    async def resolve(self, host, port=0, family=socket.AF_INET):
        try:
            resp = await self._resolver.gethostbyname(host, family)
        except aiodns.error.DNSError as exc:
            msg = exc.args[1] if len(exc.args) >= 1 else "DNS lookup failed"
            raise OSError(msg) from exc
        hosts = []
        for address in resp.addresses:
            hosts.append(
                {'hostname': host,
                 'host': address, 'port': port,
                 'family': family, 'proto': 0,
                 'flags': socket.AI_NUMERICHOST})

        if not hosts:
            raise OSError("DNS lookup failed")

        return hosts
