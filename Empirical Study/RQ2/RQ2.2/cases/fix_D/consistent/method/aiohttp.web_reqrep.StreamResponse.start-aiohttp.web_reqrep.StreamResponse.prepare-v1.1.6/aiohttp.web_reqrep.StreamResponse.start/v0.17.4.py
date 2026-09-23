    def start(self, request):
        resp_impl = self._start_pre_check(request)
        if resp_impl is not None:
            return resp_impl

        self._req = request
        keep_alive = self._keep_alive
        if keep_alive is None:
            keep_alive = request.keep_alive
        self._keep_alive = keep_alive

        resp_impl = self._resp_impl = ResponseImpl(
            request._writer,
            self._status,
            request.version,
            not keep_alive,
            self._reason)

        self._copy_cookies()

        if self._compression:
            self._start_compression(request)

        if self._chunked:
            resp_impl.enable_chunked_encoding()
            if self._chunk_size:
                resp_impl.add_chunking_filter(self._chunk_size)

        headers = self.headers.items()
        for key, val in headers:
            resp_impl.add_header(key, val)

        resp_impl.send_headers()
        return resp_impl
