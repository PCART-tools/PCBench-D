    @asyncio.coroutine
    def write(self, writer):
        """Write body."""
        if not self._parts:
            return

        for part, headers, encoding, te_encoding in self._parts:
            yield from writer.write(b'--' + self._boundary + b'\r\n')
            yield from writer.write(headers)

            if encoding or te_encoding:
                w = MultipartPayloadWriter(writer)
                if encoding:
                    w.enable_compression(encoding)
                if te_encoding:
                    w.enable_encoding(te_encoding)
                yield from part.write(w)
                yield from w.write_eof()
            else:
                yield from part.write(writer)

            yield from writer.write(b'\r\n')

        yield from writer.write(b'--' + self._boundary + b'--\r\n')
