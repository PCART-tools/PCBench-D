    @asyncio.coroutine  # pragma: no branch
    @abstractmethod
    def close(self):
        """Release resolver"""
