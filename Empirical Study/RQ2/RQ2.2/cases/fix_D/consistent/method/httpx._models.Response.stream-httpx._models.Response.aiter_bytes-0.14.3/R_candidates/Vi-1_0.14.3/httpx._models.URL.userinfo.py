    @property
    def userinfo(self) -> str:
        return self._uri_reference.userinfo or ""
