    @property
    def port(self) -> typing.Optional[int]:
        """
        The URL port as an integer.
        """
        port = self._uri_reference.port
        return int(port) if port else None
