    class HttpRequestHandler:

        def __init__(self, addr):
            if isinstance(addr, tuple):
                host, port = addr
                self.host = host
                self.port = port
            else:
                self.host = host = 'localhost'
                self.port = port = 0
            self.address = addr
            self._url = '{}://{}:{}'.format(
                'https' if use_ssl else 'http', host, port)

        def __getitem__(self, key):
            return properties[key]

        def __setitem__(self, key, value):
            properties[key] = value

        def url(self, *suffix):
            return urllib.parse.urljoin(
                self._url, '/'.join(str(s) for s in suffix))
