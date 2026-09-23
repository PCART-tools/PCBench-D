    def __init__(self, nrows, ncols, height_ratios=None, width_ratios=None):
        """
        Parameters
        ----------
        nrows, ncols : int
            The number of rows and columns of the grid.
        width_ratios : array-like of length *ncols*, optional
            Defines the relative widths of the columns. Each column gets a
            relative width of ``width_ratios[i] / sum(width_ratios)``.
            If not given, all columns will have the same width.
        height_ratios : array-like of length *nrows*, optional
            Defines the relative heights of the rows. Each column gets a
            relative height of ``height_ratios[i] / sum(height_ratios)``.
            If not given, all rows will have the same height.
        """
        self._nrows, self._ncols = nrows, ncols
        self.set_height_ratios(height_ratios)
        self.set_width_ratios(width_ratios)
