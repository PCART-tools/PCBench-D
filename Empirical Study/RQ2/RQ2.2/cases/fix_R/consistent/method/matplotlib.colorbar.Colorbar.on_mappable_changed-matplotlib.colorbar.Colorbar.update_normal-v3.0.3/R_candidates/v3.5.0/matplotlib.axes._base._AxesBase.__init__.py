    @_api.make_keyword_only("3.4", "facecolor")
    def __init__(self, fig, rect,
                 facecolor=None,  # defaults to rc axes.facecolor
                 frameon=True,
                 sharex=None,  # use Axes instance's xaxis info
                 sharey=None,  # use Axes instance's yaxis info
                 label='',
                 xscale=None,
                 yscale=None,
                 box_aspect=None,
                 **kwargs
                 ):
        """
        Build an Axes in a figure.

        Parameters
        ----------
        fig : `~matplotlib.figure.Figure`
            The Axes is built in the `.Figure` *fig*.

        rect : [left, bottom, width, height]
            The Axes is built in the rectangle *rect*. *rect* is in
            `.Figure` coordinates.

        sharex, sharey : `~.axes.Axes`, optional
            The x or y `~.matplotlib.axis` is shared with the x or
            y axis in the input `~.axes.Axes`.

        frameon : bool, default: True
            Whether the Axes frame is visible.

        box_aspect : float, optional
            Set a fixed aspect for the Axes box, i.e. the ratio of height to
            width. See `~.axes.Axes.set_box_aspect` for details.

        **kwargs
            Other optional keyword arguments:

            %(Axes:kwdoc)s

        Returns
        -------
        `~.axes.Axes`
            The new `~.axes.Axes` object.
        """

        super().__init__()
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
        self._stale_viewlims = {name: False for name in self._axis_names}
        self._sharex = sharex
        self._sharey = sharey
        self.set_label(label)
        self.set_figure(fig)
        self.set_box_aspect(box_aspect)
        self._axes_locator = None  # Optionally set via update(kwargs).
        # placeholder for any colorbars added that use this Axes.
        # (see colorbar.py):
        self._colorbars = []
        self.spines = mspines.Spines.from_dict(self._gen_axes_spines())

        # this call may differ for non-sep axes, e.g., polar
        self._init_axis()
        if facecolor is None:
            facecolor = mpl.rcParams['axes.facecolor']
        self._facecolor = facecolor
        self._frameon = frameon
        self.set_axisbelow(mpl.rcParams['axes.axisbelow'])

        self._rasterization_zorder = None
        self.cla()

        # funcs used to format x and y - fall back on major formatters
        self.fmt_xdata = None
        self.fmt_ydata = None

        self.set_navigate(True)
        self.set_navigate_mode(None)

        if xscale:
            self.set_xscale(xscale)
        if yscale:
            self.set_yscale(yscale)

        self.update(kwargs)

        for name, axis in self._get_axis_map().items():
            axis.callbacks._pickled_cids.add(
                axis.callbacks.connect(
                    'units', self._unit_change_handler(name)))

        rcParams = mpl.rcParams
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
