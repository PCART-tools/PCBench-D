    @asyncio.coroutine
    @abstractmethod
    def drain(self):
        """Flush the write buffer."""
