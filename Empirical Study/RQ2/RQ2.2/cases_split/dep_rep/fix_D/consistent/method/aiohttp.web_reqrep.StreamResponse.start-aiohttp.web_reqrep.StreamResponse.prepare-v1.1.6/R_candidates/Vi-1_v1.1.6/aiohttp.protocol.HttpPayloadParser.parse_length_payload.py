    def parse_length_payload(self, out, buf, length=0):
        """Read specified amount of bytes."""
        required = length
        while required:
            chunk = yield from buf.readsome(required)
            out.feed_data(chunk, len(chunk))
            required -= len(chunk)
