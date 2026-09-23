    @asyncio.coroutine  # pragma: no branch
    @abstractmethod
    def write(self, writer):
        """Write payload

        :param AbstractPayloadWriter writer:
        """
