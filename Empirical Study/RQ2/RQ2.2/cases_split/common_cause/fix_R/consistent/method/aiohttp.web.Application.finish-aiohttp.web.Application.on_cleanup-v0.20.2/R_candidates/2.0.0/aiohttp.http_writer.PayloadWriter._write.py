    def _write(self, chunk):
        size = len(chunk)
        self.buffer_size += size
        self.output_size += size

        if self._transport is not None:
            if self._buffer:
                self._buffer.append(chunk)
                self._transport.write(b''.join(self._buffer))
                self._buffer.clear()
            else:
                self._transport.write(chunk)
        else:
            self._buffer.append(chunk)
