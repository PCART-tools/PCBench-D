    @cache_readonly
    def hasnans(self):
        """
        Return if I have any nans; enables various perf speedups.
        """
        return bool(isna(self).any())
