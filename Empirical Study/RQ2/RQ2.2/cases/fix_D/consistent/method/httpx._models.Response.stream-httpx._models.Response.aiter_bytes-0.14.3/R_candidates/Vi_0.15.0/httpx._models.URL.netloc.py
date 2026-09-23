    @property
    def netloc(self) -> str:
        """
        Either `<host>` or `<host>:<port>` as a string.
        Always normlized to lowercase, and IDNA encoded.
        """
        host = self._uri_reference.host or ""
        port = self._uri_reference.port
        return host if port is None else f"{host}:{port}"
