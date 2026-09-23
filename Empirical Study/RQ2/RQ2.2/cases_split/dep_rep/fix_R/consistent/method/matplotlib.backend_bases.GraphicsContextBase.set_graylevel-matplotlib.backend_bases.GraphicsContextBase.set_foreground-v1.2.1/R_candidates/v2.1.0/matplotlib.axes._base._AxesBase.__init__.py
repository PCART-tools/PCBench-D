    def __init__(self, fig, rect,
                 facecolor=None,  # defaults to rc axes.facecolor
                 frameon=True,
                 sharex=None,  # use Axes instance's xaxis info
                 sharey=None,  # use Axes instance's yaxis info
                 label='',
                 xscale=None,
                 yscale=None,
                 axisbg=None,  # This will be removed eventually
                 **kwargs
                 ):
        """
        Build an :class:`Axes` instance in
        :class:`~matplotlib.figure.Figure` *fig* with
        *rect=[left, bottom, width, height]* in
        :class:`~matplotlib.figure.Figure` coordinates

        Optional keyword arguments:

          ================   =========================================
          Keyword            Description
          ================   =========================================
          *adjustable*       [ 'box' | 'datalim' | 'box-forced']
          *alpha*            float: the alpha transparency (can be None)
          *anchor*           [ 'C', 'SW', 'S', 'SE', 'E', 'NE', 'N',
                               'NW', 'W' ]
          *aspect*           [ 'auto' | 'equal' | aspect_ratio ]
          *autoscale_on*     [ *True* | *False* ] whether or not to
                             autoscale the *viewlim*
          *axisbelow*        [ *True* | *False* | 'line'] draw the grids
                             and ticks below or above most other artists,
                             or below lines but above patches
          *cursor_props*     a (*float*, *color*) tuple
          *figure*           a :class:`~matplotlib.figure.Figure`
                             instance
          *frame_on*         a boolean - draw the axes frame
          *label*            the axes label
          *navigate*         [ *True* | *False* ]
          *navigate_mode*    [ 'PAN' | 'ZOOM' | None ] the navigation
                             toolbar button status
          *position*         [left, bottom, width, height] in
                             class:`~matplotlib.figure.Figure` coords
          *sharex*           an class:`~matplotlib.axes.Axes` instance
                             to share the x-axis with
          *sharey*           an class:`~matplotlib.axes.Axes` instance
                             to share the y-axis with
          *title*            the title string
          *visible*          [ *True* | *False* ] whether the axes is
                             visible
          *xlabel*           the xlabel
          *xlim*             (*xmin*, *xmax*) view limits
          *xscale*           [%(scale)s]
          *xticklabels*      sequence of strings
          *xticks*           sequence of floats
          *ylabel*           the ylabel strings
          *ylim*             (*ymin*, *ymax*) view limits
          *yscale*           [%(scale)s]
          *yticklabels*      sequence of strings
          *yticks*           sequence of floats
          ================   =========================================
        """ % {'scale': ' | '.join(
            [repr(x) for x in mscale.get_scale_names()])}
        martist.Artist.__init__(self)
        if isinstance(rect, mtransforms.Bbox):
            self._position = rect
        else:
            self._position = mtransforms.Bbox.from_bounds(*rect)
        if self._position.width < 0 or self._position.height < 0:
            raise ValueError('Width and height specified must be non-negative')
        self._originalPosition = self._position.frozen()
        # self.set_axes(self)
        self.axes = self
        self.set_aspect('auto')
        self._adjustable = 'box'
        self.set_anchor('C')
        self._sharex = sharex
        self._sharey = sharey
        if sharex is not None:
            self._shared_x_axes.join(self, sharex)
            if sharex._adjustable == 'box':
                sharex._adjustable = 'datalim'
                # warnings.warn(
                #    'shared axes: "adjustable" is being changed to "datalim"')
            self._adjustable = 'datalim'
        if sharey is not None:
            self._shared_y_axes.join(self, sharey)
            if sharey._adjustable == 'box':
                sharey._adjustable = 'datalim'
                # warnings.warn(
                #    'shared axes: "adjustable" is being changed to "datalim"')
            self._adjustable = 'datalim'
        self.set_label(label)
        self.set_figure(fig)

        self.set_axes_locator(kwargs.get("axes_locator", None))

        self.spines = self._gen_axes_spines()

        # this call may differ for non-sep axes, e.g., polar
        self._init_axis()
        if axisbg is not None and facecolor is not None:
            raise TypeError('Both axisbg and facecolor are not None. '
                            'These keywords are aliases, only one may be '
                            'provided.')
        if axisbg is not None:
            cbook.warn_deprecated(
                '2.0', name='axisbg', alternative='facecolor')
            facecolor = axisbg
        if facecolor is None:
            facecolor = rcParams['axes.facecolor']
        self._facecolor = facecolor
        self._frameon = frameon
        self._axisbelow = rcParams['axes.axisbelow']

        self._rasterization_zorder = None

        self._hold = rcParams['axes.hold']
        if self._hold is None:
            self._hold = True

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

        if len(kwargs):
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
            left=rcParams['ytick.left'] and rcParams['ytick.minor.left'],
            right=rcParams['ytick.right'] and rcParams['ytick.minor.right'],
            which='minor')

        self.tick_params(
            top=rcParams['xtick.top'] and rcParams['xtick.major.top'],
            bottom=rcParams['xtick.bottom'] and rcParams['xtick.major.bottom'],
            left=rcParams['ytick.left'] and rcParams['ytick.major.left'],
            right=rcParams['ytick.right'] and rcParams['ytick.major.right'],
            which='major')
