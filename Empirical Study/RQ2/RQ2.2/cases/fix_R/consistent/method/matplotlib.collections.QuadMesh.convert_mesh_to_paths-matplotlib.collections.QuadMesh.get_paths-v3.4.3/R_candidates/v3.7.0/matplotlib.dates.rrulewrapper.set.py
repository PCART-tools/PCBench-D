    def set(self, **kwargs):
        """Set parameters for an existing wrapper."""
        self._construct.update(kwargs)

        self._update_rrule(**self._construct)
