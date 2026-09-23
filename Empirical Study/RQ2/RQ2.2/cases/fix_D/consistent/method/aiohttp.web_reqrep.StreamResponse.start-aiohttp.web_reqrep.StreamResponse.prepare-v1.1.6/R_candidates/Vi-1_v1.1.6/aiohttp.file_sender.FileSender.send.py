    @asyncio.coroutine
    def send(self, request, filepath):
        """Send filepath to client using request."""
        st = filepath.stat()

        modsince = request.if_modified_since
        if modsince is not None and st.st_mtime <= modsince.timestamp():
            from .web_exceptions import HTTPNotModified
            raise HTTPNotModified()

        ct, encoding = mimetypes.guess_type(str(filepath))
        if not ct:
            ct = 'application/octet-stream'

        resp = self._response_factory()
        resp.content_type = ct
        if encoding:
            resp.headers[hdrs.CONTENT_ENCODING] = encoding
        resp.last_modified = st.st_mtime

        file_size = st.st_size

        resp.content_length = file_size
        with filepath.open('rb') as f:
            yield from self._sendfile(request, resp, f, file_size)

        return resp
