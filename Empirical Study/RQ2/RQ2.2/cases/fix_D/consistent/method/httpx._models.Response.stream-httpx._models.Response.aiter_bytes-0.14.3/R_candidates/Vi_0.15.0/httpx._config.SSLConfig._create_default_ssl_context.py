    def _create_default_ssl_context(self) -> ssl.SSLContext:
        """
        Creates the default SSLContext object that's used for both verified
        and unverified connections.
        """
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        context.options |= ssl.OP_NO_SSLv2
        context.options |= ssl.OP_NO_SSLv3
        context.options |= ssl.OP_NO_TLSv1
        context.options |= ssl.OP_NO_TLSv1_1
        context.options |= ssl.OP_NO_COMPRESSION
        context.set_ciphers(DEFAULT_CIPHERS)

        if ssl.HAS_ALPN:
            alpn_idents = ["http/1.1", "h2"] if self.http2 else ["http/1.1"]
            context.set_alpn_protocols(alpn_idents)

        if hasattr(context, "keylog_filename"):  # pragma: nocover (Available in 3.8+)
            keylogfile = os.environ.get("SSLKEYLOGFILE")
            if keylogfile and self.trust_env:
                context.keylog_filename = keylogfile  # type: ignore

        return context
