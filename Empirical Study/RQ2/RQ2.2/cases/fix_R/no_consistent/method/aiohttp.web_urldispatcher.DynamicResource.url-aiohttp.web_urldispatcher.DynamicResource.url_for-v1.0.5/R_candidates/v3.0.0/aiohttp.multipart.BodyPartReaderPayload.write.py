    async def write(self, writer):
        field = self._value
        chunk = await field.read_chunk(size=2**16)
        while chunk:
            writer.write(field.decode(chunk))
            chunk = await field.read_chunk(size=2**16)
