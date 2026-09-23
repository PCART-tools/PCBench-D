    @property
    def query(self) -> bytes:
        """
        The URL query string, as raw bytes, excluding the leading b"?".
        Note that URL decoding can only be applied on URL query strings
        at the point of decoding the individual parameter names/values.
        """
        query = self._uri_reference.query or ""
        return query.encode("ascii")
