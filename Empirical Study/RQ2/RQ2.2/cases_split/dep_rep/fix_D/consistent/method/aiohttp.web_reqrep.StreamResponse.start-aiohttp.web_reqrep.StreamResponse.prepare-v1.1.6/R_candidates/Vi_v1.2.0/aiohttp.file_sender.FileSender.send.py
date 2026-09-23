    @asyncio.coroutine
    def send(self, request, filepath):
        """Send filepath to client using request."""
        gzip = False
        if 'gzip' in request.headers.get(hdrs.ACCEPT_ENCODING, ''):
            gzip_path = filepath.with_name(filepath.name + '.gz')

            if gzip_path.is_file():
                filepath = gzip_path
                gzip = True

        st = filepath.stat()

        modsince = request.if_modified_since
        if modsince is not None and st.st_mtime <= modsince.timestamp():
            raise HTTPNotModified()

        ct, encoding = mimetypes.guess_type(str(filepath))
        if not ct:
            ct = 'application/octet-stream'

        status = HTTPOk.status_code
        file_size = st.st_size
        count = file_size

        try:
            rng = request.http_range
            start = rng.start
            end = rng.stop
        except ValueError:
            raise HTTPRequestRangeNotSatisfiable

        # If a range request has been made, convert start, end slice notation
        # into file pointer offset and count
        if start is not None or end is not None:
            status = HTTPPartialContent.status_code
            if start is None and end < 0:  # return tail of file
                start = file_size + end
                count = -end
            else:
                count = (end or file_size) - start

            if start + count > file_size:
                raise HTTPRequestRangeNotSatisfiable

        resp = self._response_factory(status=status)
        resp.content_type = ct
        if encoding:
            resp.headers[hdrs.CONTENT_ENCODING] = encoding
        if gzip:
            resp.headers[hdrs.VARY] = hdrs.ACCEPT_ENCODING
        resp.last_modified = st.st_mtime

        resp.content_length = count
        with filepath.open('rb') as f:
            if start:
                f.seek(start)
            yield from self._sendfile(request, resp, f, count)

        return resp
