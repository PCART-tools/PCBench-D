    def __call__(self):
        return self._handler(
            self, self._app, self._router, self._time_service, loop=self._loop,
            secure_proxy_ssl_header=self._secure_proxy_ssl_header,
            **self._kwargs)
