    def set_agg_filter(self, filter_func):
        """
        set agg_filter function.

        """
        self._agg_filter = filter_func
        self.stale = True
