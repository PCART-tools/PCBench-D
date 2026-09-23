    def buffer_data(self, chunk):
        if chunk:
            size = len(chunk)
            self.buffer_size += size
            self.output_size += size
            self._buffer.append(chunk)
