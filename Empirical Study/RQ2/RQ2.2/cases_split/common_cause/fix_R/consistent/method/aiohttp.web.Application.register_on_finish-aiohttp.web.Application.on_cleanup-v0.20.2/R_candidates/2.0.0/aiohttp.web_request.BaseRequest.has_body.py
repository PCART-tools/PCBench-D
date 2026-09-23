    @property
    def has_body(self):
        """Return True if request has HTTP BODY, False otherwise."""
        return not self._payload.at_eof()
