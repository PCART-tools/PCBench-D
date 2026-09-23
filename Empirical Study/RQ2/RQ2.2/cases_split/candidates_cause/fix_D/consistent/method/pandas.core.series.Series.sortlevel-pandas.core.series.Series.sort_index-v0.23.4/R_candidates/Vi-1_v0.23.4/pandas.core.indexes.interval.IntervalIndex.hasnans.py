    @cache_readonly
    def hasnans(self):
        """
        Return if the IntervalIndex has any nans; enables various performance
        speedups
        """
        return self._isnan.any()
