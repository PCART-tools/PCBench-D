    @property
    def npoints(self):
        """
        The number of non- ``fill_value`` points.

        Examples
        --------
        >>> s = SparseArray([0, 0, 1, 1, 1], fill_value=0)
        >>> s.npoints
        3
        """
        return self.sp_index.npoints
