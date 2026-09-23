    async def write(self, writer):
        """Write body."""
        if not self._parts:
            return

        for part, headers, encoding, te_encoding in self._parts:
            await writer.write(b'--' + self._boundary + b'\r\n')
            await writer.write(headers)

            if encoding or te_encoding:
                w = MultipartPayloadWriter(writer)
                if encoding:
                    w.enable_compression(encoding)
                if te_encoding:
                    w.enable_encoding(te_encoding)
                await part.write(w)
                await w.write_eof()
            else:
                await part.write(writer)

            await writer.write(b'\r\n')

        await writer.write(b'--' + self._boundary + b'--\r\n')
