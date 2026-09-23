    def _start(self, request,
               HttpVersion10=HttpVersion10,
               HttpVersion11=HttpVersion11,
               CONNECTION=hdrs.CONNECTION,
               DATE=hdrs.DATE,
               SERVER=hdrs.SERVER,
               SET_COOKIE=hdrs.SET_COOKIE,
               TRANSFER_ENCODING=hdrs.TRANSFER_ENCODING):
        self._req = request
        keep_alive = self._keep_alive
        if keep_alive is None:
            keep_alive = request.keep_alive
        self._keep_alive = keep_alive
        version = request.version

        resp_impl = self._resp_impl = ResponseImpl(
            request._writer,
            self._status,
            version,
            not keep_alive,
            self._reason)

        headers = self.headers
        for cookie in self._cookies.values():
            value = cookie.output(header='')[1:]
            headers.add(SET_COOKIE, value)

        if self._compression:
            self._start_compression(request)

        if self._chunked:
            if request.version != HttpVersion11:
                raise RuntimeError("Using chunked encoding is forbidden "
                                   "for HTTP/{0.major}.{0.minor}".format(
                                       request.version))
            resp_impl.chunked = True
            if self._chunk_size:
                resp_impl.add_chunking_filter(self._chunk_size)
            headers[TRANSFER_ENCODING] = 'chunked'
        else:
            resp_impl.length = self.content_length

        headers.setdefault(DATE, request._time_service.strtime())
        headers.setdefault(SERVER, resp_impl.SERVER_SOFTWARE)
        if CONNECTION not in headers:
            if keep_alive:
                if version == HttpVersion10:
                    headers[CONNECTION] = 'keep-alive'
            else:
                if version == HttpVersion11:
                    headers[CONNECTION] = 'close'

        resp_impl.headers = headers

        self._send_headers(resp_impl)
        self._task = request._task
        return resp_impl
