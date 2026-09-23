    @asyncio.coroutine
    def prepare(self, request):
        filepath = self._path

        gzip = False
        if 'gzip' in request.headers.get(hdrs.ACCEPT_ENCODING, ''):
            gzip_path = filepath.with_name(filepath.name + '.gz')

            if gzip_path.is_file():
                filepath = gzip_path
                gzip = True

        st = filepath.stat()

        modsince = request.if_modified_since
        if modsince is not None and st.st_mtime <= modsince.timestamp():
            self.set_status(HTTPNotModified.status_code)
            return (yield from super().prepare(request))

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
            self.set_status(HTTPRequestRangeNotSatisfiable.status_code)
            return (yield from super().prepare(request))

        # If a range request has been made, convert start, end slice notation
        # into file pointer offset and count
        if start is not None or end is not None:
            if start is None and end < 0:  # return tail of file
                start = file_size + end
                count = -end
            else:
                count = (end or file_size) - start

            if start + count > file_size:
                # rfc7233:If the last-byte-pos value is
                # absent, or if the value is greater than or equal to
                # the current length of the representation data,
                # the byte range is interpreted as the remainder
                # of the representation (i.e., the server replaces the
                # value of last-byte-pos with a value that is one less than
                # the current length of the selected representation).
                count = file_size - start

            if start >= file_size:
                count = 0

        if count != file_size:
            status = HTTPPartialContent.status_code

        self.set_status(status)
        self.content_type = ct
        if encoding:
            self.headers[hdrs.CONTENT_ENCODING] = encoding
        if gzip:
            self.headers[hdrs.VARY] = hdrs.ACCEPT_ENCODING
        self.last_modified = st.st_mtime
        self.content_length = count

        if count:
            with filepath.open('rb') as fobj:
                if start:
                    fobj.seek(start)

                return (yield from self._sendfile(request, fobj, count))

        return (yield from super().prepare(request))
