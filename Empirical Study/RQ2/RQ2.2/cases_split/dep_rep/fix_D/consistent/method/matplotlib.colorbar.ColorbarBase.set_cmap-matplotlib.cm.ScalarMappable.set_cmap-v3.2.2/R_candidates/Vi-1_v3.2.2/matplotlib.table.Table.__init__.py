    def __init__(self, ax, loc=None, bbox=None, **kwargs):
        """
        Parameters
        ----------
        ax : `matplotlib.axes.Axes`
            The `~.axes.Axes` to plot the table into.
        loc : str
            The position of the cell with respect to *ax*. This must be one of
            the `~.Table.codes`.
        bbox : `.Bbox` or None
            A bounding box to draw the table into. If this is not *None*, this
            overrides *loc*.

        Other Parameters
        ----------------
        **kwargs
            `.Artist` properties.
        """

        Artist.__init__(self)

        if isinstance(loc, str):
            if loc not in self.codes:
                cbook.warn_deprecated(
                    "3.1", message="Unrecognized location {!r}. Falling back "
                    "on 'bottom'; valid locations are\n\t{}\n"
                    "This will raise an exception %(removal)s."
                    .format(loc, '\n\t'.join(self.codes)))
                loc = 'bottom'
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
        self.update(kwargs)

        self.set_clip_on(False)
