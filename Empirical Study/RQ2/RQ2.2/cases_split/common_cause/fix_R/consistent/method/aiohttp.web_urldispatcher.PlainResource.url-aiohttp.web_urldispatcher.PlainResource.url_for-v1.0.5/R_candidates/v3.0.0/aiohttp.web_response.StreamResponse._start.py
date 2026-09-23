    def _start(self, request,
               HttpVersion10=HttpVersion10,
               HttpVersion11=HttpVersion11,
               CONNECTION=hdrs.CONNECTION,
               DATE=hdrs.DATE,
               SERVER=hdrs.SERVER,
               CONTENT_TYPE=hdrs.CONTENT_TYPE,
               CONTENT_LENGTH=hdrs.CONTENT_LENGTH,
               SET_COOKIE=hdrs.SET_COOKIE,
               SERVER_SOFTWARE=SERVER_SOFTWARE,
               TRANSFER_ENCODING=hdrs.TRANSFER_ENCODING):
        self._req = request

        keep_alive = self._keep_alive
        if keep_alive is None:
            keep_alive = request.keep_alive
        self._keep_alive = keep_alive

        version = request.version
        writer = self._payload_writer = request._payload_writer

        headers = self._headers
        for cookie in self._cookies.values():
            value = cookie.output(header='')[1:]
            headers.add(SET_COOKIE, value)

        if self._compression:
            self._start_compression(request)

        if self._chunked:
            if version != HttpVersion11:
                raise RuntimeError(
                    "Using chunked encoding is forbidden "
                    "for HTTP/{0.major}.{0.minor}".format(request.version))
            writer.enable_chunking()
            headers[TRANSFER_ENCODING] = 'chunked'
            if CONTENT_LENGTH in headers:
                del headers[CONTENT_LENGTH]
        elif self._length_check:
            writer.length = self.content_length
            if writer.length is None:
                if version >= HttpVersion11:
                    writer.enable_chunking()
                    headers[TRANSFER_ENCODING] = 'chunked'
                    if CONTENT_LENGTH in headers:
                        del headers[CONTENT_LENGTH]
                else:
                    keep_alive = False

        headers.setdefault(CONTENT_TYPE, 'application/octet-stream')
        headers.setdefault(DATE, rfc822_formatted_time())
        headers.setdefault(SERVER, SERVER_SOFTWARE)

        # connection header
        if CONNECTION not in headers:
            if keep_alive:
                if version == HttpVersion10:
                    headers[CONNECTION] = 'keep-alive'
            else:
                if version == HttpVersion11:
                    headers[CONNECTION] = 'close'

        # status line
        status_line = 'HTTP/{}.{} {} {}\r\n'.format(
            version[0], version[1], self._status, self._reason)
        writer.write_headers(status_line, headers)

        return writer
