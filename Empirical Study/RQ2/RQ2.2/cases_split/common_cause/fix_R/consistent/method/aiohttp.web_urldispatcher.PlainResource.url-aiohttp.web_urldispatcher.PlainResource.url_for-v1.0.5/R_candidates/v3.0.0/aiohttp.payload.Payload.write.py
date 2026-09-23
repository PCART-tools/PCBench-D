    @abstractmethod
    async def write(self, writer):
        """Write payload.

        writer is an AbstractStreamWriter instance:
        """
