    def __init__(self, loop=None, *args, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()

        if aiodns is None:
            raise RuntimeError("Resolver requires aiodns library")

        self._loop = loop
        self._resolver = aiodns.DNSResolver(*args, loop=loop, **kwargs)

        if not hasattr(self._resolver, 'gethostbyname'):
            # aiodns 1.1 is not available, fallback to DNSResolver.query
            self.resolve = self.resolve_with_query
