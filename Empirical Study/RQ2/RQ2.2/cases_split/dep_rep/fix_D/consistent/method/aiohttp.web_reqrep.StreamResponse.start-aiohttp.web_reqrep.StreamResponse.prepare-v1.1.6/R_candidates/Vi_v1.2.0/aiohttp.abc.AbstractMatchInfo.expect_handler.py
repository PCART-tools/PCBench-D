    @asyncio.coroutine  # pragma: no branch
    @abstractmethod
    def expect_handler(self, request):
        """Expect handler for 100-continue processing"""
