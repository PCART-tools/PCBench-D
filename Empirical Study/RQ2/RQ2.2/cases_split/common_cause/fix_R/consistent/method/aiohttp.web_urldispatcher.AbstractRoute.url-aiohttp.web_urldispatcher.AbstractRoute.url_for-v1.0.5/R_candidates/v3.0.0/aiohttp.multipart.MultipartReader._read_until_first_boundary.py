    async def _read_until_first_boundary(self):
        while True:
            chunk = await self._readline()
            if chunk == b'':
                raise ValueError("Could not find starting boundary %r"
                                 % (self._boundary))
            chunk = chunk.rstrip()
            if chunk == self._boundary:
                return
            elif chunk == self._boundary + b'--':
                self._at_eof = True
                return
