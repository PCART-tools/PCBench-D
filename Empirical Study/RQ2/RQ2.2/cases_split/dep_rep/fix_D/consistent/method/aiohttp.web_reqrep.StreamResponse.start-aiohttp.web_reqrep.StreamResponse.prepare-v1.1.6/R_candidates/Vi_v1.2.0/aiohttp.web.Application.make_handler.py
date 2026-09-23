    def make_handler(self, *, secure_proxy_ssl_header=None, **kwargs):
        debug = kwargs.pop('debug', sentinel)
        if debug is not sentinel:
            warnings.warn(
                "`debug` parameter is deprecated. "
                "Use Application's debug mode instead", DeprecationWarning)
            if debug != self.debug:
                raise ValueError(
                    "The value of `debug` parameter conflicts with the debug "
                    "settings of the `Application` instance. The "
                    "application's debug mode setting should be used instead "
                    "as a single point to setup a debug mode. For more "
                    "information please check "
                    "http://aiohttp.readthedocs.io/en/stable/"
                    "web_reference.html#aiohttp.web.Application"
                )
        self.freeze()
        self._secure_proxy_ssl_header = secure_proxy_ssl_header
        return Server(self._handle, request_factory=self._make_request,
                      debug=self.debug, loop=self.loop, **kwargs)
