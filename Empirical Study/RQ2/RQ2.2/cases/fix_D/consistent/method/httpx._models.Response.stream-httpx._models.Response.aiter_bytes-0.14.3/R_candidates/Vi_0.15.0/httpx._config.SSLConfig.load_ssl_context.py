    def load_ssl_context(self) -> ssl.SSLContext:
        logger.trace(
            f"load_ssl_context "
            f"verify={self.verify!r} "
            f"cert={self.cert!r} "
            f"trust_env={self.trust_env!r} "
            f"http2={self.http2!r}"
        )

        if self.verify:
            return self.load_ssl_context_verify()
        return self.load_ssl_context_no_verify()
