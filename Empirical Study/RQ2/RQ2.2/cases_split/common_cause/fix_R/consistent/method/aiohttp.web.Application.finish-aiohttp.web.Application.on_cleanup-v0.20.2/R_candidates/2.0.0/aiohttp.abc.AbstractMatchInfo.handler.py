    @asyncio.coroutine  # pragma: no branch
    @abstractmethod
    def handler(self, request):
        """Execute matched request handler"""
