    @cache_readonly
    def hasnans(self):
        """ return if I have any nans; enables various perf speedups """
        if self._can_hold_na:
            return self._isnan.any()
        else:
            return False
