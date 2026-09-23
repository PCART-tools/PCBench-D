    @property
    def userinfo(self) -> bytes:
        """
        The URL userinfo as a raw bytestring.
        For example: b"jo%40email.com:a%20secret".
        """
        userinfo = self._uri_reference.userinfo or ""
        return userinfo.encode("ascii")
