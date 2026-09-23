    def _write_eof_payload(self):
        while True:
            try:
                chunk = yield
            except aiohttp.EofStream:
                break

            self.transport.write(chunk)
            self.output_length += len(chunk)
