    @property
    def host(self) -> str:
        return self._uri_reference.host or ""
