    @reify
    def _scheme(self):
        if self._transport.get_extra_info('sslcontext'):
            return 'https'
        secure_proxy_ssl_header = self._secure_proxy_ssl_header
        if secure_proxy_ssl_header is not None:
            header, value = secure_proxy_ssl_header
            if self.headers.get(header) == value:
                return 'https'
        return 'http'
