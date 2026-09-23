    def __init__(self, ax, cmap=None,
                 norm=None,
                 alpha=None,
                 values=None,
                 boundaries=None,
                 orientation='vertical',
                 ticklocation='auto',
                 extend='neither',
                 spacing='uniform',  # uniform or proportional
                 ticks=None,
                 format=None,
                 drawedges=False,
                 filled=True,
                 extendfrac=None,
                 extendrect=False,
                 label='',
                 ):
        #: The axes that this colorbar lives in.
        self.ax = ax
        self._patch_ax()
        if cmap is None:
            cmap = cm.get_cmap()
        if norm is None:
            norm = colors.Normalize()
        self.alpha = alpha
        cm.ScalarMappable.__init__(self, cmap=cmap, norm=norm)
        self.values = values
        self.boundaries = boundaries
        self.extend = extend
        self._inside = self._slice_dict[extend]
        self.spacing = spacing
        self.orientation = orientation
        self.drawedges = drawedges
        self.filled = filled
        self.extendfrac = extendfrac
        self.extendrect = extendrect
        self.solids = None
        self.lines = list()
        self.outline = None
        self.patch = None
        self.dividers = None

        if ticklocation == 'auto':
            ticklocation = 'bottom' if orientation == 'horizontal' else 'right'
        self.ticklocation = ticklocation

        self.set_label(label)
        if cbook.iterable(ticks):
            self.locator = ticker.FixedLocator(ticks, nbins=len(ticks))
        else:
            self.locator = ticks    # Handle default in _ticker()
        if format is None:
            if isinstance(self.norm, colors.LogNorm):
                self.formatter = ticker.LogFormatterSciNotation()
            elif isinstance(self.norm, colors.SymLogNorm):
                self.formatter = ticker.LogFormatterSciNotation(
                                        linthresh=self.norm.linthresh)
            else:
                self.formatter = ticker.ScalarFormatter()
        elif isinstance(format, six.string_types):
            self.formatter = ticker.FormatStrFormatter(format)
        else:
            self.formatter = format  # Assume it is a Formatter
        # The rest is in a method so we can recalculate when clim changes.
        self.config_axis()
        self.draw_all()
