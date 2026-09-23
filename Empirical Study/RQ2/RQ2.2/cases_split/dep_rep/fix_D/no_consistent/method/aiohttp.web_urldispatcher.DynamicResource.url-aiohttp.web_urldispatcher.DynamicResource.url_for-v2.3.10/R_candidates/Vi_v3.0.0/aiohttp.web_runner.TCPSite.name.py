    @property
    def name(self):
        scheme = 'https' if self._ssl_context else 'http'
        return str(URL.build(scheme=scheme, host=self._host, port=self._port))
