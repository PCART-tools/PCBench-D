    @asyncio.coroutine
    @abstractmethod
    def write_eof(self, chunk=b''):
        """Write last chunk"""
