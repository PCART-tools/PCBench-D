    @cache_readonly
    def hasnans(self):
        """ return if I have any nans; enables various perf speedups """
        return (self.asi8 == tslib.iNaT).any()
