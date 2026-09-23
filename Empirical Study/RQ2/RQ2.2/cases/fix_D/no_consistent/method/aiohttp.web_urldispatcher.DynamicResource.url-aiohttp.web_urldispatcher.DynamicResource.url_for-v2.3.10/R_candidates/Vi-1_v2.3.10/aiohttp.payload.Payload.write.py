    @asyncio.coroutine  # pragma: no branch
    @abstractmethod
    def write(self, writer):
        """Write payload.

        writer is an AbstractPayloadWriter instance:
        """
