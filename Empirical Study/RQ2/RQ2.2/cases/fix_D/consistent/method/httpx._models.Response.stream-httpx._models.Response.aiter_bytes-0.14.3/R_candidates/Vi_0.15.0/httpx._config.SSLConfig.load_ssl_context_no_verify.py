    def load_ssl_context_no_verify(self) -> ssl.SSLContext:
        """
        Return an SSL context for unverified connections.
        """
        context = self._create_default_ssl_context()
        context.verify_mode = ssl.CERT_NONE
        context.check_hostname = False
        self._load_client_certs(context)
        return context
