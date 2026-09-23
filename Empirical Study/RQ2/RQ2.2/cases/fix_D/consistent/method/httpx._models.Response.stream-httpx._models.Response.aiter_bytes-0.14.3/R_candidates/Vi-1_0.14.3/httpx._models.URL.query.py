    @property
    def query(self) -> str:
        return self._uri_reference.query or ""
