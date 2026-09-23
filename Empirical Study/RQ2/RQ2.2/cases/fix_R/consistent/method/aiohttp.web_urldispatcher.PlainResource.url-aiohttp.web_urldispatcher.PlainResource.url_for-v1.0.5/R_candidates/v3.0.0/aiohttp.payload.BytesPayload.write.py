    async def write(self, writer):
        await writer.write(self._value)
