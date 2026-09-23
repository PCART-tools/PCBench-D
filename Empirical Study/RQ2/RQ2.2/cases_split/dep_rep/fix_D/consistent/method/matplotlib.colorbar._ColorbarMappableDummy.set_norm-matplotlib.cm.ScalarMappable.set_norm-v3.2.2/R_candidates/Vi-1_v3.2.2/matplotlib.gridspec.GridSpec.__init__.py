    def __init__(self, nrows, ncols, figure=None,
                 left=None, bottom=None, right=None, top=None,
                 wspace=None, hspace=None,
                 width_ratios=None, height_ratios=None):
        """
        Parameters
        ----------
        nrows, ncols : int
            The number of rows and columns of the grid.

        figure : `~.figure.Figure`, optional
            Only used for constrained layout to create a proper layoutbox.

        left, right, top, bottom : float, optional
            Extent of the subplots as a fraction of figure width or height.
            Left cannot be larger than right, and bottom cannot be larger than
            top. If not given, the values will be inferred from a figure or
            rcParams at draw time. See also `GridSpec.get_subplot_params`.

        wspace : float, optional
            The amount of width reserved for space between subplots,
            expressed as a fraction of the average axis width.
            If not given, the values will be inferred from a figure or
            rcParams when necessary. See also `GridSpec.get_subplot_params`.

        hspace : float, optional
            The amount of height reserved for space between subplots,
            expressed as a fraction of the average axis height.
            If not given, the values will be inferred from a figure or
            rcParams when necessary. See also `GridSpec.get_subplot_params`.

        width_ratios : array-like of length *ncols*, optional
            Defines the relative widths of the columns. Each column gets a
            relative width of ``width_ratios[i] / sum(width_ratios)``.
            If not given, all columns will have the same width.

        height_ratios : array-like of length *nrows*, optional
            Defines the relative heights of the rows. Each column gets a
            relative height of ``height_ratios[i] / sum(height_ratios)``.
            If not given, all rows will have the same height.

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
