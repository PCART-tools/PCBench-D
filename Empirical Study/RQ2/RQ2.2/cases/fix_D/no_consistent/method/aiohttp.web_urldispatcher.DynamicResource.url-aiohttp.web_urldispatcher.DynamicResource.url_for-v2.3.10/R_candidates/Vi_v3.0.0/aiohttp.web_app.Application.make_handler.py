    def make_handler(self, *,
                     loop=None,
                     access_log_class=AccessLogger,
                     **kwargs):

        if not issubclass(access_log_class, AbstractAccessLogger):
            raise TypeError(
                'access_log_class must be subclass of '
                'aiohttp.abc.AbstractAccessLogger, got {}'.format(
                    access_log_class))

        self._set_loop(loop)
        self.freeze()

        kwargs['debug'] = self.debug
        if self._handler_args:
            for k, v in self._handler_args.items():
                kwargs[k] = v

        return Server(self._handle, request_factory=self._make_request,
                      access_log_class=access_log_class,
                      loop=self.loop, **kwargs)
