    def send(self, conn):
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

        writer = PayloadWriter(conn.writer, self.loop)

        if self.compress:
            writer.enable_compression(self.compress)

        if self.chunked is not None:
            writer.enable_chunking()

        # set default content-type
        if (self.method in self.POST_METHODS and
                hdrs.CONTENT_TYPE not in self.skip_auto_headers and
                hdrs.CONTENT_TYPE not in self.headers):
            self.headers[hdrs.CONTENT_TYPE] = 'application/octet-stream'

        # set the connection header
        connection = self.headers.get(hdrs.CONNECTION)
        if not connection:
            if self.keep_alive():
                if self.version == HttpVersion10:
                    connection = 'keep-alive'
            else:
                if self.version == HttpVersion11:
                    connection = 'close'

        if connection is not None:
            self.headers[hdrs.CONNECTION] = connection

        # status + headers
        status_line = '{0} {1} HTTP/{2[0]}.{2[1]}\r\n'.format(
            self.method, path, self.version)
        writer.write_headers(status_line, self.headers)

        self._writer = helpers.ensure_future(
            self.write_bytes(writer, conn), loop=self.loop)

        self.response = self.response_class(
            self.method, self.original_url,
            writer=self._writer, continue100=self._continue, timer=self._timer)

        self.response._post_init(self.loop)
        return self.response
