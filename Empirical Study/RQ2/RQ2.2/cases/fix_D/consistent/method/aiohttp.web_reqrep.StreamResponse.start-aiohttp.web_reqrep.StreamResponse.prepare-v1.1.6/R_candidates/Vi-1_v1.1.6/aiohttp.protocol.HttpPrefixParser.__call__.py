    def __call__(self, out, buf):
        raw_data = yield from buf.waituntil(b' ', 12)
        method = raw_data.decode('ascii', 'surrogateescape').strip()

        # method
        method = method.upper()
        if not METHRE.match(method):
            raise errors.BadStatusLine(method)

        # allowed method
        if self.allowed_methods and method not in self.allowed_methods:
            raise errors.HttpMethodNotAllowed(message=method)

        out.feed_data(method, len(method))
        out.feed_eof()
