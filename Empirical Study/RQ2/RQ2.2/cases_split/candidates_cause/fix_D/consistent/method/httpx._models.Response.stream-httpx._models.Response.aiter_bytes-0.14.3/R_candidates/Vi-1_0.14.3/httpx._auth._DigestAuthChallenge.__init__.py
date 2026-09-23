    def __init__(
        self,
        realm: bytes,
        nonce: bytes,
        algorithm: str,
        opaque: typing.Optional[bytes] = None,
        qop: typing.Optional[bytes] = None,
    ) -> None:
        self.realm = realm
        self.nonce = nonce
        self.algorithm = algorithm
        self.opaque = opaque
        self.qop = qop
