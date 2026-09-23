    def send(self, writer, reader):
        # Specify request target:
        # - CONNECT request must send authority form URI
        # - not CONNECT proxy must send absolute form URI
        # - most common is origin form URI
        if self.method == hdrs.METH_CONNECT:
            path = '{}:{}'.format(self.url.raw_host, self.url.port)
        elif self.proxy and not self.ssl:
            path = str(self.url)
        else:
            path = self.url.raw_path
            if self.url.raw_query_string:
                path += '?' + self.url.raw_query_string

        request = aiohttp.Request(writer, self.method, path,
                                  self.version)

        if self.compress:
            request.add_compression_filter(self.compress)

        if self.chunked is not None:
            request.enable_chunked_encoding()
            request.add_chunking_filter(self.chunked)

        # set default content-type
        if (self.method in self.POST_METHODS and
                hdrs.CONTENT_TYPE not in self.skip_auto_headers and
                hdrs.CONTENT_TYPE not in self.headers):
            self.headers[hdrs.CONTENT_TYPE] = 'application/octet-stream'

        for k, value in self.headers.items():
            request.add_header(k, value)
        request.send_headers()

        self._writer = helpers.ensure_future(
            self.write_bytes(request, reader), loop=self.loop)

        self.response = self.response_class(
            self.method, self.url,
            writer=self._writer, continue100=self._continue,
            timeout=self._timeout)
        self.response._post_init(self.loop)
        return self.response
