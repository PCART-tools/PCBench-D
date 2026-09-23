    @property
    def port(self) -> typing.Optional[int]:
        port = self._uri_reference.port
        return int(port) if port else None
