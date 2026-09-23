    def make_handler(self, *, loop=None,
                     secure_proxy_ssl_header=None, **kwargs):
        self._set_loop(loop)
        self.freeze()

        kwargs['debug'] = self.debug
        if self._handler_args:
            for k, v in self._handler_args.items():
                kwargs[k] = v

        self._secure_proxy_ssl_header = secure_proxy_ssl_header
        return Server(self._handle, request_factory=self._make_request,
                      loop=self.loop, **kwargs)
