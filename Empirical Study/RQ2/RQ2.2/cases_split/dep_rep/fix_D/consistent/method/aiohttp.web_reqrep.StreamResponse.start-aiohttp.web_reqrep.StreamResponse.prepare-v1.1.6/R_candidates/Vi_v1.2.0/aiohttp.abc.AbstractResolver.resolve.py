    @asyncio.coroutine  # pragma: no branch
    @abstractmethod
    def resolve(self, hostname):
        """Return IP address for given hostname"""
