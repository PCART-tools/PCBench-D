    @abstractmethod
    async def expect_handler(self, request):
        """Expect handler for 100-continue processing"""
