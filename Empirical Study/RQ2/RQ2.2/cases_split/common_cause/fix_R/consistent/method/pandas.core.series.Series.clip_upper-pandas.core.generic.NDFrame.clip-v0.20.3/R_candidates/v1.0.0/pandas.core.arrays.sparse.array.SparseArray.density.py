    @property
    def density(self):
        """
        The percent of non- ``fill_value`` points, as decimal.

        Examples
        --------
        >>> s = SparseArray([0, 0, 1, 1, 1], fill_value=0)
        >>> s.density
        0.6
        """
        r = float(self.sp_index.npoints) / float(self.sp_index.length)
        return r
