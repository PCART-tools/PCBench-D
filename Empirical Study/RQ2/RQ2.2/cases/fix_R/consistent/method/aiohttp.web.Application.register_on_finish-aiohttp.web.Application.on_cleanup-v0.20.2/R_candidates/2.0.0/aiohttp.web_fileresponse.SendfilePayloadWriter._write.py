    def _write(self, chunk):
        self.output_size += len(chunk)
        self._buffer.append(chunk)
