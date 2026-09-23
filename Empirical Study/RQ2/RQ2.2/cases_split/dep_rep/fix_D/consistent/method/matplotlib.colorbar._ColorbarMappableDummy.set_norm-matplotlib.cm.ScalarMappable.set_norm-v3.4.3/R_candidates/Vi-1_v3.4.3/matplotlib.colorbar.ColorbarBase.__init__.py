    @_api.make_keyword_only("3.3", "cmap")
    def __init__(self, ax, cmap=None,
                 norm=None,
                 alpha=None,
                 values=None,
                 boundaries=None,
                 orientation='vertical',
                 ticklocation='auto',
                 extend=None,
                 spacing='uniform',  # uniform or proportional
                 ticks=None,
                 format=None,
                 drawedges=False,
                 filled=True,
                 extendfrac=None,
                 extendrect=False,
                 label='',
                 ):
        _api.check_isinstance([colors.Colormap, None], cmap=cmap)
        _api.check_in_list(
            ['vertical', 'horizontal'], orientation=orientation)
        _api.check_in_list(
            ['auto', 'left', 'right', 'top', 'bottom'],
            ticklocation=ticklocation)
        _api.check_in_list(
            ['uniform', 'proportional'], spacing=spacing)

        self.ax = ax
        # Bind some methods to the axes to warn users against using them.
        ax.set_xticks = ax.set_yticks = _set_ticks_on_axis_warn
        ax.set(navigate=False)

        if cmap is None:
            cmap = cm.get_cmap()
        if norm is None:
            norm = colors.Normalize()
        if extend is None:
            if hasattr(norm, 'extend'):
                extend = norm.extend
            else:
                extend = 'neither'
        self.alpha = alpha
        self.cmap = cmap
        self.norm = norm
        self.values = values
        self.boundaries = boundaries
        self.extend = extend
        self._inside = _api.check_getitem(
            {'neither': slice(0, None), 'both': slice(1, -1),
             'min': slice(1, None), 'max': slice(0, -1)},
            extend=extend)
        self.spacing = spacing
        self.orientation = orientation
        self.drawedges = drawedges
        self.filled = filled
        self.extendfrac = extendfrac
        self.extendrect = extendrect
        self.solids = None
        self.solids_patches = []
        self.lines = []

        for spine in ax.spines.values():
            spine.set_visible(False)
        self.outline = ax.spines['outline'] = _ColorbarSpine(ax)

        self.patch = mpatches.Polygon(
            np.empty((0, 2)),
            color=mpl.rcParams['axes.facecolor'], linewidth=0.01, zorder=-1)
        ax.add_artist(self.patch)

        self.dividers = collections.LineCollection(
            [],
            colors=[mpl.rcParams['axes.edgecolor']],
            linewidths=[0.5 * mpl.rcParams['axes.linewidth']])
        self.ax.add_collection(self.dividers)

        self.locator = None
        self.formatter = None
        self._manual_tick_data_values = None
        self.__scale = None  # linear, log10 for now.  Hopefully more?

        if ticklocation == 'auto':
            ticklocation = 'bottom' if orientation == 'horizontal' else 'right'
        self.ticklocation = ticklocation

        self.set_label(label)
        self._reset_locator_formatter_scale()

        if np.iterable(ticks):
            self.locator = ticker.FixedLocator(ticks, nbins=len(ticks))
        else:
            self.locator = ticks    # Handle default in _ticker()

        if isinstance(format, str):
            self.formatter = ticker.FormatStrFormatter(format)
        else:
            self.formatter = format  # Assume it is a Formatter or None
        self.draw_all()
