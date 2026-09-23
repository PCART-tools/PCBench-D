    def __init__(self, nrows, ncols, height_ratios=None, width_ratios=None):
        """
        The number of rows and number of columns of the grid need to
        be set. Optionally, the ratio of heights and widths of rows and
        columns can be specified.
        """
        self._nrows, self._ncols = nrows, ncols
        self.set_height_ratios(height_ratios)
        self.set_width_ratios(width_ratios)
