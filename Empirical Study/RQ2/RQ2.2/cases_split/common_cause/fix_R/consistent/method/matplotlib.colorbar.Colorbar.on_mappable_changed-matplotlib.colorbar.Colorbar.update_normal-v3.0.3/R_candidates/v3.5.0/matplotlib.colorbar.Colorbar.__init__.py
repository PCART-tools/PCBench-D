    def __init__(self, ax, mappable=None, *, cmap=None,
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

        if mappable is None:
            mappable = cm.ScalarMappable(norm=norm, cmap=cmap)

        # Ensure the given mappable's norm has appropriate vmin and vmax
        # set even if mappable.draw has not yet been called.
        if mappable.get_array() is not None:
            mappable.autoscale_None()

        self.mappable = mappable
        cmap = mappable.cmap
        norm = mappable.norm

        if isinstance(mappable, contour.ContourSet):
            cs = mappable
            alpha = cs.get_alpha()
            boundaries = cs._levels
            values = cs.cvalues
            extend = cs.extend
            filled = cs.filled
            if ticks is None:
                ticks = ticker.FixedLocator(cs.levels, nbins=10)
        elif isinstance(mappable, martist.Artist):
            alpha = mappable.get_alpha()

        mappable.colorbar = self
        mappable.colorbar_cid = mappable.callbacks.connect(
            'changed', self.update_normal)

        _api.check_in_list(
            ['vertical', 'horizontal'], orientation=orientation)
        _api.check_in_list(
            ['auto', 'left', 'right', 'top', 'bottom'],
            ticklocation=ticklocation)
        _api.check_in_list(
            ['uniform', 'proportional'], spacing=spacing)

        self.ax = ax
        self.ax._axes_locator = _ColorbarAxesLocator(self)

        if extend is None:
            if (not isinstance(mappable, contour.ContourSet)
                    and getattr(cmap, 'colorbar_extend', False) is not False):
                extend = cmap.colorbar_extend
            elif hasattr(norm, 'extend'):
                extend = norm.extend
            else:
                extend = 'neither'
        self.alpha = None
        # Call set_alpha to handle array-like alphas properly
        self.set_alpha(alpha)
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

        for spine in self.ax.spines.values():
            spine.set_visible(False)
        self.outline = self.ax.spines['outline'] = _ColorbarSpine(self.ax)
        self._short_axis().set_visible(False)
        # Only kept for backcompat; remove after deprecation of .patch elapses.
        self._patch = mpatches.Polygon(
            np.empty((0, 2)),
            color=mpl.rcParams['axes.facecolor'], linewidth=0.01, zorder=-1)
        ax.add_artist(self._patch)

        self.dividers = collections.LineCollection(
            [],
            colors=[mpl.rcParams['axes.edgecolor']],
            linewidths=[0.5 * mpl.rcParams['axes.linewidth']])
        self.ax.add_collection(self.dividers)

        self.locator = None
        self.minorlocator = None
        self.formatter = None
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

        if isinstance(mappable, contour.ContourSet) and not mappable.filled:
            self.add_lines(mappable)

        # Link the Axes and Colorbar for interactive use
        self.ax._colorbar = self
        # Don't navigate on any of these types of mappables
        if (isinstance(self.norm, (colors.BoundaryNorm, colors.NoNorm)) or
                isinstance(self.mappable, contour.ContourSet)):
            self.ax.set_navigate(False)

        # These are the functions that set up interactivity on this colorbar
        self._interactive_funcs = ["_get_view", "_set_view",
                                   "_set_view_from_bbox", "drag_pan"]
        for x in self._interactive_funcs:
            setattr(self.ax, x, getattr(self, x))
        # Set the cla function to the cbar's method to override it
        self.ax.cla = self._cbar_cla
