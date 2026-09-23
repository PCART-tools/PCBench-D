    def _write_length_payload(self, length):
        """Write specified number of bytes to a stream."""
        while True:
            try:
                chunk = yield
            except aiohttp.EofStream:
                break

            if length:
                l = len(chunk)
                if length >= l:
                    self.transport.write(chunk)
                    self.output_length += l
                    length = length-l
                else:
                    self.transport.write(chunk[:length])
                    self.output_length += length
                    length = 0
