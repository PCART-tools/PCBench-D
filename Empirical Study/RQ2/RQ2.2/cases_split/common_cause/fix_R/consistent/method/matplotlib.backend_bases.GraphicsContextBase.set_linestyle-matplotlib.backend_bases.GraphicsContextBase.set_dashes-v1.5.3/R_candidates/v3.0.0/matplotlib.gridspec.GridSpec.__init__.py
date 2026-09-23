    def __init__(self, nrows, ncols, figure=None,
                 left=None, bottom=None, right=None, top=None,
                 wspace=None, hspace=None,
                 width_ratios=None, height_ratios=None):
        """
        The number of rows and number of columns of the grid need to be set.
        Optionally, the subplot layout parameters (e.g., left, right, etc.)
        can be tuned.

        Parameters
        ----------
        nrows : int
            Number of rows in grid.

        ncols : int
            Number or columns in grid.

        figure : ~.figure.Figure, optional

        left, right, top, bottom : float
            Extent of the subplots as a fraction of figure width or height.
            Left cannot be larger than right, and bottom cannot be larger than
            top.

        wspace : float
            The amount of width reserved for space between subplots,
            expressed as a fraction of the average axis width.

        hspace : float
            The amount of height reserved for space between subplots,
            expressed as a fraction of the average axis height.

        Notes
        -----
        See `~.figure.SubplotParams` for descriptions of the layout parameters.
        """
        self.left = left
        self.bottom = bottom
        self.right = right
        self.top = top
        self.wspace = wspace
        self.hspace = hspace
        self.figure = figure

        GridSpecBase.__init__(self, nrows, ncols,
                              width_ratios=width_ratios,
                              height_ratios=height_ratios)

        if self.figure is None or not self.figure.get_constrained_layout():
            self._layoutbox = None
        else:
            self.figure.init_layoutbox()
            self._layoutbox = layoutbox.LayoutBox(
                parent=self.figure._layoutbox,
                name='gridspec' + layoutbox.seq_id(),
                artist=self)
