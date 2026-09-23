    @asyncio.coroutine
    def drain(self):
        """Flush the write buffer.

        The intended use is to write

          w.write(data)
          yield from w.drain()
        """
        if self._protocol.transport is not None:
            yield from self._protocol._drain_helper()
