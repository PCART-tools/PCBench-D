    def __init__(
        self,
        *,
        cert: CertTypes = None,
        verify: VerifyTypes = True,
        trust_env: bool = None,
        http2: bool = False,
    ):
        self.cert = cert
        self.verify = verify
        self.trust_env = trust_env
        self.http2 = http2
        self.ssl_context = self.load_ssl_context()
