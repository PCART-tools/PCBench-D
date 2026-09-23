    @cache_readonly
    def hasnans(self):
        """
        Return if I have any nans; enables various perf speedups.
        """
        if self._can_hold_na:
            return bool(self._isnan.any())
        else:
            return False
