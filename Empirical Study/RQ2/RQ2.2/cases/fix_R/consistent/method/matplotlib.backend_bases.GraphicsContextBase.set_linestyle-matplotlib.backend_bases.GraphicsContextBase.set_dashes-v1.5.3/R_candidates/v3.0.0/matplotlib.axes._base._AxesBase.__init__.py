    def __init__(self, fig, rect,
                 facecolor=None,  # defaults to rc axes.facecolor
                 frameon=True,
                 sharex=None,  # use Axes instance's xaxis info
                 sharey=None,  # use Axes instance's yaxis info
                 label='',
                 xscale=None,
                 yscale=None,
                 **kwargs
                 ):
        """
        Build an axes in a figure.

        Parameters
        ----------
        fig : `~matplotlib.figure.Figure`
            The axes is build in the `.Figure` *fig*.

        rect : [left, bottom, width, height]
            The axes is build in the rectangle *rect*. *rect* is in
            `.Figure` coordinates.

        sharex, sharey : `~.axes.Axes`, optional
            The x or y `~.matplotlib.axis` is shared with the x or
            y axis in the input `~.axes.Axes`.

        frameon : bool, optional
            True means that the axes frame is visible.

        **kwargs
            Other optional keyword arguments:
            %(Axes)s

        Returns
        -------
        axes : `~.axes.Axes`
            The new `~.axes.Axes` object.
        """

        martist.Artist.__init__(self)
        if isinstance(rect, mtransforms.Bbox):
            self._position = rect
        else:
            self._position = mtransforms.Bbox.from_bounds(*rect)
        if self._position.width < 0 or self._position.height < 0:
            raise ValueError('Width and height specified must be non-negative')
        self._originalPosition = self._position.frozen()
        self.axes = self
        self._aspect = 'auto'
        self._adjustable = 'box'
        self._anchor = 'C'
        self._sharex = sharex
        self._sharey = sharey
        if sharex is not None:
            self._shared_x_axes.join(self, sharex)
        if sharey is not None:
            self._shared_y_axes.join(self, sharey)
        self.set_label(label)
        self.set_figure(fig)

        self.set_axes_locator(kwargs.get("axes_locator", None))

        self.spines = self._gen_axes_spines()

        # this call may differ for non-sep axes, e.g., polar
        self._init_axis()
        if facecolor is None:
            facecolor = rcParams['axes.facecolor']
        self._facecolor = facecolor
        self._frameon = frameon
        self.set_axisbelow(rcParams['axes.axisbelow'])

        self._rasterization_zorder = None
        self._connected = {}  # a dict from events to (id, func)
        self.cla()

        # funcs used to format x and y - fall back on major formatters
        self.fmt_xdata = None
        self.fmt_ydata = None

        self._cachedRenderer = None
        self.set_navigate(True)
        self.set_navigate_mode(None)

        if xscale:
            self.set_xscale(xscale)
        if yscale:
            self.set_yscale(yscale)

        self.update(kwargs)

        if self.xaxis is not None:
            self._xcid = self.xaxis.callbacks.connect(
                'units finalize', lambda: self._on_units_changed(scalex=True))

        if self.yaxis is not None:
            self._ycid = self.yaxis.callbacks.connect(
                'units finalize', lambda: self._on_units_changed(scaley=True))

        self.tick_params(
            top=rcParams['xtick.top'] and rcParams['xtick.minor.top'],
            bottom=rcParams['xtick.bottom'] and rcParams['xtick.minor.bottom'],
            labeltop=(rcParams['xtick.labeltop'] and
                      rcParams['xtick.minor.top']),
            labelbottom=(rcParams['xtick.labelbottom'] and
                         rcParams['xtick.minor.bottom']),
            left=rcParams['ytick.left'] and rcParams['ytick.minor.left'],
            right=rcParams['ytick.right'] and rcParams['ytick.minor.right'],
            labelleft=(rcParams['ytick.labelleft'] and
                       rcParams['ytick.minor.left']),
            labelright=(rcParams['ytick.labelright'] and
                        rcParams['ytick.minor.right']),
            which='minor')

        self.tick_params(
            top=rcParams['xtick.top'] and rcParams['xtick.major.top'],
            bottom=rcParams['xtick.bottom'] and rcParams['xtick.major.bottom'],
            labeltop=(rcParams['xtick.labeltop'] and
                      rcParams['xtick.major.top']),
            labelbottom=(rcParams['xtick.labelbottom'] and
                         rcParams['xtick.major.bottom']),
            left=rcParams['ytick.left'] and rcParams['ytick.major.left'],
            right=rcParams['ytick.right'] and rcParams['ytick.major.right'],
            labelleft=(rcParams['ytick.labelleft'] and
                       rcParams['ytick.major.left']),
            labelright=(rcParams['ytick.labelright'] and
                        rcParams['ytick.major.right']),
            which='major')

        self._layoutbox = None
        self._poslayoutbox = None
