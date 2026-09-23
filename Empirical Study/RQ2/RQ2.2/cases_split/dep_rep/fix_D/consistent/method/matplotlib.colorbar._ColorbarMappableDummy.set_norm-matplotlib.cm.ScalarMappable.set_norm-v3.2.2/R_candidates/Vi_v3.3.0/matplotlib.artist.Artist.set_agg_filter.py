    def set_agg_filter(self, filter_func):
        """
        Set the agg filter.

        Parameters
        ----------
        filter_func : callable
            A filter function, which takes a (m, n, 3) float array and a dpi
            value, and returns a (m, n, 3) array.

            .. ACCEPTS: a filter function, which takes a (m, n, 3) float array
                and a dpi value, and returns a (m, n, 3) array
        """
        self._agg_filter = filter_func
        self.stale = True
