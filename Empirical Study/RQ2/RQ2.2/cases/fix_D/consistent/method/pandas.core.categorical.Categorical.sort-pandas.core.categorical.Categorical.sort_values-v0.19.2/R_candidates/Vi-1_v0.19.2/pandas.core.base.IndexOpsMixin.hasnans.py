    @cache_readonly
    def hasnans(self):
        """ return if I have any nans; enables various perf speedups """
        return isnull(self).any()
