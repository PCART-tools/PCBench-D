    @wrap_payload_filter
    def add_chunking_filter(self, chunk_size=16*1024, *,
                            EOF_MARKER=EOF_MARKER, EOL_MARKER=EOL_MARKER):
        """Split incoming stream into chunks."""
        buf = bytearray()
        chunk = yield

        while True:
            if chunk is EOF_MARKER:
                if buf:
                    yield buf

                yield EOF_MARKER

            else:
                buf.extend(chunk)

                while len(buf) >= chunk_size:
                    chunk = bytes(buf[:chunk_size])
                    del buf[:chunk_size]
                    yield chunk

                chunk = yield EOL_MARKER
