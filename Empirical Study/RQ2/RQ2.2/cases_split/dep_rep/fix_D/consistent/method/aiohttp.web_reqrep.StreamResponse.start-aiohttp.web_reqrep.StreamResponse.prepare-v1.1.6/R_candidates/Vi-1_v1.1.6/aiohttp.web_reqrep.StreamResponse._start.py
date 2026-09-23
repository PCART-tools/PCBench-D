    def _start(self, request):
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

        self._copy_cookies()

        headers = self.headers
        if self._compression:
            self._start_compression(request)

        if self._chunked:
            if request.version != HttpVersion11:
                raise RuntimeError("Using chunked encoding is forbidden "
                                   "for HTTP/{0.major}.{0.minor}".format(
                                       request.version))
            resp_impl.enable_chunked_encoding()
            if self._chunk_size:
                resp_impl.add_chunking_filter(self._chunk_size)
            headers[hdrs.TRANSFER_ENCODING] = 'chunked'
        else:
            resp_impl.length = self.content_length

        if hdrs.DATE not in headers:
            headers[hdrs.DATE] = request._time_service.strtime()
        headers.setdefault(hdrs.SERVER, resp_impl.SERVER_SOFTWARE)
        if hdrs.CONNECTION not in headers:
            if keep_alive:
                if version == HttpVersion10:
                    headers[hdrs.CONNECTION] = 'keep-alive'
            else:
                if version == HttpVersion11:
                    headers[hdrs.CONNECTION] = 'close'

        resp_impl.headers = headers

        self._send_headers(resp_impl)
        return resp_impl
