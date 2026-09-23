    def _validate_monotonic(self):
        """
        Validate on is_monotonic.
        """
        if not self._on.is_monotonic:
            formatted = self.on or 'index'
            raise ValueError("{0} must be "
                             "monotonic".format(formatted))
