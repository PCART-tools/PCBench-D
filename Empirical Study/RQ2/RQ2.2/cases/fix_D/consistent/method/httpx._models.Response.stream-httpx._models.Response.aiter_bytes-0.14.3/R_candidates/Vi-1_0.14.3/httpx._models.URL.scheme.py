    @property
    def scheme(self) -> str:
        return self._uri_reference.scheme or ""
