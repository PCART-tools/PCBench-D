    def _get_ssl_context(self, req):
        """Logic to get the correct SSL context

        0. if req.ssl is false, return None

        1. if ssl_context is specified in req, use it
        2. if _ssl_context is specified in self, use it
        3. otherwise:
            1. if verify_ssl is not specified in req, use self.ssl_context
               (will generate a default context according to self.verify_ssl)
            2. if verify_ssl is True in req, generate a default SSL context
            3. if verify_ssl is False in req, generate a SSL context that
               won't verify
        """
        if req.is_ssl():
            if ssl is None:  # pragma: no cover
                raise RuntimeError('SSL is not supported.')
            sslcontext = req.ssl
            if isinstance(sslcontext, ssl.SSLContext):
                return sslcontext
            if sslcontext is not None:
                # not verified or fingerprinted
                return self._make_ssl_context(False)
            sslcontext = self._ssl
            if isinstance(sslcontext, ssl.SSLContext):
                return sslcontext
            if sslcontext is not None:
                # not verified or fingerprinted
                return self._make_ssl_context(False)
            return self._make_ssl_context(True)
        else:
            return None
