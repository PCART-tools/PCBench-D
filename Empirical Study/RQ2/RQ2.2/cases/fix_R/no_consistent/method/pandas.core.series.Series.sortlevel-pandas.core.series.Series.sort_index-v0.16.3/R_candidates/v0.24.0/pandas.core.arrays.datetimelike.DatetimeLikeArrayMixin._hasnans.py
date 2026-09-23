    @property  # NB: override with cache_readonly in immutable subclasses
    def _hasnans(self):
        """
        return if I have any nans; enables various perf speedups
        """
        return bool(self._isnan.any())
