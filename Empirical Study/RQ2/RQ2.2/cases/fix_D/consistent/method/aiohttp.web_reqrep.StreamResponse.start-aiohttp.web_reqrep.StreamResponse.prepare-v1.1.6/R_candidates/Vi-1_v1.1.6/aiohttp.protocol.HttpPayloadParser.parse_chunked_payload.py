    def parse_chunked_payload(self, out, buf):
        """Chunked transfer encoding parser."""
        while True:
            # read next chunk size
            line = yield from buf.readuntil(b'\r\n', 8192)

            i = line.find(b';')
            if i >= 0:
                line = line[:i]  # strip chunk-extensions
            else:
                line = line.strip()
            try:
                size = int(line, 16)
            except ValueError:
                raise errors.TransferEncodingError(line) from None

            if size == 0:  # eof marker
                break

            # read chunk and feed buffer
            while size:
                chunk = yield from buf.readsome(size)
                out.feed_data(chunk, len(chunk))
                size = size - len(chunk)

            # toss the CRLF at the end of the chunk
            yield from buf.skip(2)

        # read and discard trailer up to the CRLF terminator
        yield from buf.skipuntil(b'\r\n')
