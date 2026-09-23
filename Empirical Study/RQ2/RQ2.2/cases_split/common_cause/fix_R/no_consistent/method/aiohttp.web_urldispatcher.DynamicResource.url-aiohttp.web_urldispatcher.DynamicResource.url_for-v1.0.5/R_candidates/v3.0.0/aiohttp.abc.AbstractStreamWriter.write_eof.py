    @abstractmethod
    async def write_eof(self, chunk=b''):
        """Write last chunk."""
