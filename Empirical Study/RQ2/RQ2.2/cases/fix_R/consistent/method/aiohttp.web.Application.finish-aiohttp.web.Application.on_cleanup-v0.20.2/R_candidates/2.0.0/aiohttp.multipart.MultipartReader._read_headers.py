    @asyncio.coroutine
    def _read_headers(self):
        lines = [b'']
        while True:
            chunk = yield from self._content.readline()
            chunk = chunk.strip()
            lines.append(chunk)
            if not chunk:
                break
        parser = HttpParser()
        headers, *_ = parser.parse_headers(lines)
        return headers
