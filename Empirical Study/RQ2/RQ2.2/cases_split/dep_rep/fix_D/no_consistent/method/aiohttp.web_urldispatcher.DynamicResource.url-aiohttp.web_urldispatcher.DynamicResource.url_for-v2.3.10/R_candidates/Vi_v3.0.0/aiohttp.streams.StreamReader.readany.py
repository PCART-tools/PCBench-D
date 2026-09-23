    async def readany(self):
        if self._exception is not None:
            raise self._exception

        if not self._buffer and not self._eof:
            await self._wait('readany')

        return self._read_nowait(-1)
