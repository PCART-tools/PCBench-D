    @property
    def can_read_body(self):
        """Return True if request's HTTP BODY can be read, False otherwise."""
        return not self._payload.at_eof()
