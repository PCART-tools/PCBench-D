    def parse_eof_payload(self, out, buf):
        """Read all bytes until eof."""
        try:
            while True:
                chunk = yield from buf.readsome()
                out.feed_data(chunk, len(chunk))
        except aiohttp.EofStream:
            pass
