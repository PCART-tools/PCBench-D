    async def send_str(self, data, compress=None):
        if not isinstance(data, str):
            raise TypeError('data argument must be str (%r)' % type(data))
        await self._writer.send(data, binary=False, compress=compress)
