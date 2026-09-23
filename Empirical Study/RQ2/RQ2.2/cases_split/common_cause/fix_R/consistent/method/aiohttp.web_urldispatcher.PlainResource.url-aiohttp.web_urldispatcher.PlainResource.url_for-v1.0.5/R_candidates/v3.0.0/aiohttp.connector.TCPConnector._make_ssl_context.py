    @staticmethod
    @functools.lru_cache(None)
    def _make_ssl_context(verified):
        if verified:
            return ssl.create_default_context()
        else:
            sslcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            sslcontext.options |= ssl.OP_NO_SSLv2
            sslcontext.options |= ssl.OP_NO_SSLv3
            sslcontext.options |= ssl.OP_NO_COMPRESSION
            sslcontext.set_default_verify_paths()
            return sslcontext
