    def _parse_challenge(
        self, request: Request, response: Response, auth_header: str
    ) -> "_DigestAuthChallenge":
        """
        Returns a challenge from a Digest WWW-Authenticate header.
        These take the form of:
        `Digest realm="realm@host.com",qop="auth,auth-int",nonce="abc",opaque="xyz"`
        """
        scheme, _, fields = auth_header.partition(" ")

        # This method should only ever have been called with a Digest auth header.
        assert scheme.lower() == "digest"

        header_dict: typing.Dict[str, str] = {}
        for field in parse_http_list(fields):
            key, value = field.strip().split("=", 1)
            header_dict[key] = unquote(value)

        try:
            realm = header_dict["realm"].encode()
            nonce = header_dict["nonce"].encode()
            qop = header_dict["qop"].encode() if "qop" in header_dict else None
            opaque = header_dict["opaque"].encode() if "opaque" in header_dict else None
            algorithm = header_dict.get("algorithm", "MD5")
            return _DigestAuthChallenge(
                realm=realm, nonce=nonce, qop=qop, opaque=opaque, algorithm=algorithm
            )
        except KeyError as exc:
            message = "Malformed Digest WWW-Authenticate header"
            raise ProtocolError(message, request=request) from exc
