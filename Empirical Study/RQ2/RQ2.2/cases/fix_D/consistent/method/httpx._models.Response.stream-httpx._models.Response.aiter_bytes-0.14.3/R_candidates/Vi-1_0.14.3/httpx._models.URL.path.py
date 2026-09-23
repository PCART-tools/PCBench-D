    @property
    def path(self) -> str:
        return self._uri_reference.path or "/"
