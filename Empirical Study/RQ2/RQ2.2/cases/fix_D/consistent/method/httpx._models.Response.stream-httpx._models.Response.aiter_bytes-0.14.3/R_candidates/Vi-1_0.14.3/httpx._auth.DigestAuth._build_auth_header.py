    def _build_auth_header(
        self, request: Request, challenge: "_DigestAuthChallenge"
    ) -> str:
        hash_func = self._ALGORITHM_TO_HASH_FUNCTION[challenge.algorithm]

        def digest(data: bytes) -> bytes:
            return hash_func(data).hexdigest().encode()

        A1 = b":".join((self._username, challenge.realm, self._password))

        path = request.url.full_path.encode("utf-8")
        A2 = b":".join((request.method.encode(), path))
        # TODO: implement auth-int
        HA2 = digest(A2)

        nonce_count = 1  # TODO: implement nonce counting
        nc_value = b"%08x" % nonce_count
        cnonce = self._get_client_nonce(nonce_count, challenge.nonce)

        HA1 = digest(A1)
        if challenge.algorithm.lower().endswith("-sess"):
            HA1 = digest(b":".join((HA1, challenge.nonce, cnonce)))

        qop = self._resolve_qop(challenge.qop, request=request)
        if qop is None:
            digest_data = [HA1, challenge.nonce, HA2]
        else:
            digest_data = [challenge.nonce, nc_value, cnonce, qop, HA2]
        key_digest = b":".join(digest_data)

        format_args = {
            "username": self._username,
            "realm": challenge.realm,
            "nonce": challenge.nonce,
            "uri": path,
            "response": digest(b":".join((HA1, key_digest))),
            "algorithm": challenge.algorithm.encode(),
        }
        if challenge.opaque:
            format_args["opaque"] = challenge.opaque
        if qop:
            format_args["qop"] = b"auth"
            format_args["nc"] = nc_value
            format_args["cnonce"] = cnonce

        return "Digest " + self._get_header_value(format_args)
