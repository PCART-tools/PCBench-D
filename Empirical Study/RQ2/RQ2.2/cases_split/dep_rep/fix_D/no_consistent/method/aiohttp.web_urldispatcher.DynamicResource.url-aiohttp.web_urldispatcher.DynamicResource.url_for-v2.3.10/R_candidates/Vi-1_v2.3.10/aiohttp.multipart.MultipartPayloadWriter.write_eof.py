    @asyncio.coroutine
    def write_eof(self):
        if self._compress is not None:
            chunk = self._compress.flush()
            if chunk:
                self._compress = None
                yield from self.write(chunk)

        if self._encoding == 'base64':
            if self._encoding_buffer:
                yield from self._writer.write(base64.b64encode(
                    self._encoding_buffer))
