    @asyncio.coroutine
    def json(self, *, encoding=None, loads=json.loads):
        """Read and decodes JSON response."""
        if self._content is None:
            yield from self.read()

        ctype = self.headers.get(hdrs.CONTENT_TYPE, '').lower()
        if 'json' not in ctype:
            client_logger.warning(
                'Attempt to decode JSON with unexpected mimetype: %s', ctype)

        stripped = self._content.strip()
        if not stripped:
            return None

        if encoding is None:
            encoding = self._get_encoding()

        return loads(stripped.decode(encoding))
