    def _get_loc_only_exact_matches(self, key):
        """
        This is overriden on subclasses (namely, IntervalIndex) to control
        get_slice_bound.
        """
        return self.get_loc(key)
