    async def write(self, writer):
        try:
            chunk = self._value.read(DEFAULT_LIMIT)
            while chunk:
                await writer.write(chunk)
                chunk = self._value.read(DEFAULT_LIMIT)
        finally:
            self._value.close()
