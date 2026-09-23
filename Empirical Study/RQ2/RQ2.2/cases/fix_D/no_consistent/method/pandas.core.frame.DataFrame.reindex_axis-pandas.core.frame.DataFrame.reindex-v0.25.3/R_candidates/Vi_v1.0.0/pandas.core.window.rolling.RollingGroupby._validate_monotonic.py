    def _validate_monotonic(self):
        """
        Validate that on is monotonic;
        we don't care for groupby.rolling
        because we have already validated at a higher
        level.
        """
        pass
