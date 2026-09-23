    @property
    def ssl_context(self):
        """SSLContext instance for https requests.

        Lazy property, creates context on demand.
        """
        if ssl is None:  # pragma: no cover
            raise RuntimeError('SSL is not supported.')

        if self._ssl_context is None:
            if not self._verify_ssl:
                sslcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
                sslcontext.options |= ssl.OP_NO_SSLv2
                sslcontext.options |= ssl.OP_NO_SSLv3
                sslcontext.options |= _SSL_OP_NO_COMPRESSION
                sslcontext.set_default_verify_paths()
            else:
                sslcontext = ssl.create_default_context()
            self._ssl_context = sslcontext
        return self._ssl_context
