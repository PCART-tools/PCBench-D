    def _write(self, chunk):
        size = len(chunk)
        self.buffer_size += size
        self.output_size += size

        if self._transport is None or self._transport.is_closing():
            raise asyncio.CancelledError('Cannot write to closing transport')
        self._transport.write(chunk)
