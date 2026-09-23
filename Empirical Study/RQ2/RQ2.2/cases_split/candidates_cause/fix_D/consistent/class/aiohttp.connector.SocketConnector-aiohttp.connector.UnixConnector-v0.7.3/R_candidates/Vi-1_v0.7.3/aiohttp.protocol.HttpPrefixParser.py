class HttpPrefixParser:
    """Waits for 'HTTP' prefix (non destructive)"""

    def __init__(self, allowed_methods=()):
        self.allowed_methods = [m.upper() for m in allowed_methods]

    def __call__(self, out, buf):
        try:
            raw_data = yield from buf.waituntil(b' ', 24)
            method = raw_data.decode('ascii', 'surrogateescape').strip()

            # method
            method = method.upper()
            if not METHRE.match(method):
                raise errors.BadStatusLine(method)

            # allowed method
            if self.allowed_methods and method not in self.allowed_methods:
                raise errors.HttpMethodNotAllowed(method)

            out.feed_data(method)
            out.feed_eof()
        except aiohttp.EofStream:
            # Presumably, the server closed the connection before
            # sending a valid response.
            pass
