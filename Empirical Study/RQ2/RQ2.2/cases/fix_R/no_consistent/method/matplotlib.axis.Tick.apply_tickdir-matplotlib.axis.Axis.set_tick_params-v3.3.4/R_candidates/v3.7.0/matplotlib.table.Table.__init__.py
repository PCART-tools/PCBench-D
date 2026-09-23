    def __init__(self, ax, loc=None, bbox=None, **kwargs):
        """
        Parameters
        ----------
        ax : `matplotlib.axes.Axes`
            The `~.axes.Axes` to plot the table into.
        loc : str
            The position of the cell with respect to *ax*. This must be one of
            the `~.Table.codes`.
        bbox : `.Bbox` or [xmin, ymin, width, height], optional
            A bounding box to draw the table into. If this is not *None*, this
            overrides *loc*.

        Other Parameters
        ----------------
        **kwargs
            `.Artist` properties.
        """

        super().__init__()

        if isinstance(loc, str):
            if loc not in self.codes:
                raise ValueError(
                    "Unrecognized location {!r}. Valid locations are\n\t{}"
                    .format(loc, '\n\t'.join(self.codes)))
            loc = self.codes[loc]
        self.set_figure(ax.figure)
        self._axes = ax
        self._loc = loc
        self._bbox = bbox

        # use axes coords
        ax._unstale_viewLim()
        self.set_transform(ax.transAxes)

        self._cells = {}
        self._edges = None
        self._autoColumns = []
        self._autoFontsize = True
        self._internal_update(kwargs)

        self.set_clip_on(False)
