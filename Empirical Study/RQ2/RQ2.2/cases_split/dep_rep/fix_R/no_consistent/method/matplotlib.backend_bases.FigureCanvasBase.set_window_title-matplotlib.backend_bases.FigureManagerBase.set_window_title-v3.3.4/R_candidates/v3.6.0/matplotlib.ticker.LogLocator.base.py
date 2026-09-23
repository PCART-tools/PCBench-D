    @_api.deprecated("3.6", alternative='set_params(base=...)')
    def base(self, base):
        """Set the log base (major tick every ``base**i``, i integer)."""
        self._base = float(base)
