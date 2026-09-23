    @asyncio.coroutine
    def json(self, *, encoding=None, loads=json.loads,
             content_type='application/json'):
        """Read and decodes JSON response."""
        if self._content is None:
            yield from self.read()

        if content_type:
            ctype = self.headers.get(hdrs.CONTENT_TYPE, '').lower()
            if content_type not in ctype:
                raise ClientResponseError(
                    message=('Attempt to decode JSON with '
                             'unexpected mimetype: %s' % ctype),
                    headers=self.headers)

        stripped = self._content.strip()
        if not stripped:
            return None

        if encoding is None:
            encoding = self._get_encoding()

        return loads(stripped.decode(encoding))
