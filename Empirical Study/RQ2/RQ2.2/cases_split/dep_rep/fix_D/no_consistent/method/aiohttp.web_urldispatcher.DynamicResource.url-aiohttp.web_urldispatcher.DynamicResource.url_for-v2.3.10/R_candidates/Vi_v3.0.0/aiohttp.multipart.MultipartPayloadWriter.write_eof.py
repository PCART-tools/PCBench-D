    async def write_eof(self):
        if self._compress is not None:
            chunk = self._compress.flush()
            if chunk:
                self._compress = None
                await self.write(chunk)

        if self._encoding == 'base64':
            if self._encoding_buffer:
                await self._writer.write(base64.b64encode(
                    self._encoding_buffer))
