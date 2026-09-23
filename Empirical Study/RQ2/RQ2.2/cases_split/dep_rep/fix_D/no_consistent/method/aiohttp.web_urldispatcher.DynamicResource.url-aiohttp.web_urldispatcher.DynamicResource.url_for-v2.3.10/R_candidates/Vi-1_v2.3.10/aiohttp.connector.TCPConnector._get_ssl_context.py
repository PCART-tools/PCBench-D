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
        if req.ssl:
            sslcontext = req.ssl_context or self._ssl_context
            if not sslcontext:
                if req.verify_ssl is None:
                    sslcontext = self.ssl_context
                elif req.verify_ssl:
                    sslcontext = ssl.create_default_context()
                else:
                    sslcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
                    sslcontext.options |= ssl.OP_NO_SSLv2
                    sslcontext.options |= ssl.OP_NO_SSLv3
                    sslcontext.options |= _SSL_OP_NO_COMPRESSION
                    sslcontext.set_default_verify_paths()
        else:
            sslcontext = None
        return sslcontext
