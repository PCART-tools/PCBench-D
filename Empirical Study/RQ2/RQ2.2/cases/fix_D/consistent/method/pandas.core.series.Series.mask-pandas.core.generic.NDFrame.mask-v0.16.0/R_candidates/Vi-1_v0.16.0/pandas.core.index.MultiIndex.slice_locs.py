    def slice_locs(self, start=None, end=None, step=None, kind=None):
        """
        For an ordered MultiIndex, compute the slice locations for input
        labels. They can be tuples representing partial levels, e.g. for a
        MultiIndex with 3 levels, you can pass a single value (corresponding to
        the first level), or a 1-, 2-, or 3-tuple.

        Parameters
        ----------
        start : label or tuple, default None
            If None, defaults to the beginning
        end : label or tuple
            If None, defaults to the end
        step : int or None
            Slice step
        kind : string, optional, defaults None

        Returns
        -------
        (start, end) : (int, int)

        Notes
        -----
        This function assumes that the data is sorted by the first level
        """
        # This function adds nothing to its parent implementation (the magic
        # happens in get_slice_bound method), but it adds meaningful doc.
        return super(MultiIndex, self).slice_locs(start, end, step, kind=kind)
