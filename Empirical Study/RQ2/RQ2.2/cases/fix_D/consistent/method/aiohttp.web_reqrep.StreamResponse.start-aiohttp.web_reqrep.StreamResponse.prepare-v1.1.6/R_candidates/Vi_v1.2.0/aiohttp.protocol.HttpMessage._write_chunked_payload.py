    def _write_chunked_payload(self):
        """Write data in chunked transfer encoding."""
        while True:
            try:
                chunk = yield
            except aiohttp.EofStream:
                self.transport.write(b'0\r\n\r\n')
                self.output_length += 5
                break

            chunk = bytes(chunk)
            chunk_len = '{:x}\r\n'.format(len(chunk)).encode('ascii')
            self.transport.write(chunk_len + chunk + b'\r\n')
            self.output_length += len(chunk_len) + len(chunk) + 2
