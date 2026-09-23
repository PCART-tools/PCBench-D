    @reify
    def cookies(self):
        """Return request cookies.

        A read-only dictionary-like object.
        """
        raw = self.headers.get(hdrs.COOKIE, '')
        parsed = http.cookies.SimpleCookie(raw)
        return MappingProxyType(
            {key: val.value for key, val in parsed.items()})
