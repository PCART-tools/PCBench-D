    @property
    def has_body(self):
        """Return True if request's HTTP BODY can be read, False otherwise."""
        warnings.warn(
            "Deprecated, use .can_read_body #2005",
            DeprecationWarning, stacklevel=2)
        return not self._payload.at_eof()
