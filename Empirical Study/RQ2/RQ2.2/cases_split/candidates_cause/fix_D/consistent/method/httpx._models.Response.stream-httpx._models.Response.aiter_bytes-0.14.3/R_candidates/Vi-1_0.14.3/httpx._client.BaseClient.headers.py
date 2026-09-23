    @headers.setter
    def headers(self, headers: HeaderTypes) -> None:
        self._headers = Headers(headers)
