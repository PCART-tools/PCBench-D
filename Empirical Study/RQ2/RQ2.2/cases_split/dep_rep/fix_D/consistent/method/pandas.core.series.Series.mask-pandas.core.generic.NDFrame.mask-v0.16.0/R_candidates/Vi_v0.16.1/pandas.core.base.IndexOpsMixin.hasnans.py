    def hasnans(self):
        """ return if I have any nans; enables various perf speedups """
        return com.isnull(self).any()
