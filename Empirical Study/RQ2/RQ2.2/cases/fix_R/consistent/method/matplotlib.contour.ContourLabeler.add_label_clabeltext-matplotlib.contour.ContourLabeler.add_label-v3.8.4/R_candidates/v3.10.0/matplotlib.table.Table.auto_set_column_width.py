    def auto_set_column_width(self, col):
        """
        Automatically set the widths of given columns to optimal sizes.

        Parameters
        ----------
        col : int or sequence of ints
            The indices of the columns to auto-scale.
        """
        col1d = np.atleast_1d(col)
        if not np.issubdtype(col1d.dtype, np.integer):
            raise TypeError("col must be an int or sequence of ints.")
        for cell in col1d:
            self._autoColumns.append(cell)

        self.stale = True
