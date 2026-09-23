    def __init__(self, xdata, ydata, *,
                 linewidth=None,  # all Nones default to rc
                 linestyle=None,
                 color=None,
                 gapcolor=None,
                 marker=None,
                 markersize=None,
                 markeredgewidth=None,
                 markeredgecolor=None,
                 markerfacecolor=None,
                 markerfacecoloralt='none',
                 fillstyle=None,
                 antialiased=None,
                 dash_capstyle=None,
                 solid_capstyle=None,
                 dash_joinstyle=None,
                 solid_joinstyle=None,
                 pickradius=5,
                 drawstyle=None,
                 markevery=None,
                 **kwargs
                 ):
        """
        Create a `.Line2D` instance with *x* and *y* data in sequences of
        *xdata*, *ydata*.

        Additional keyword arguments are `.Line2D` properties:

        %(Line2D:kwdoc)s

        See :meth:`set_linestyle` for a description of the line styles,
        :meth:`set_marker` for a description of the markers, and
        :meth:`set_drawstyle` for a description of the draw styles.

        """
        super().__init__()

        # Convert sequences to NumPy arrays.
        if not np.iterable(xdata):
            raise RuntimeError('xdata must be a sequence')
        if not np.iterable(ydata):
            raise RuntimeError('ydata must be a sequence')

        if linewidth is None:
            linewidth = mpl.rcParams['lines.linewidth']

        if linestyle is None:
            linestyle = mpl.rcParams['lines.linestyle']
        if marker is None:
            marker = mpl.rcParams['lines.marker']
        if color is None:
            color = mpl.rcParams['lines.color']

        if markersize is None:
            markersize = mpl.rcParams['lines.markersize']
        if antialiased is None:
            antialiased = mpl.rcParams['lines.antialiased']
        if dash_capstyle is None:
            dash_capstyle = mpl.rcParams['lines.dash_capstyle']
        if dash_joinstyle is None:
            dash_joinstyle = mpl.rcParams['lines.dash_joinstyle']
        if solid_capstyle is None:
            solid_capstyle = mpl.rcParams['lines.solid_capstyle']
        if solid_joinstyle is None:
            solid_joinstyle = mpl.rcParams['lines.solid_joinstyle']

        if drawstyle is None:
            drawstyle = 'default'

        self._dashcapstyle = None
        self._dashjoinstyle = None
        self._solidjoinstyle = None
        self._solidcapstyle = None
        self.set_dash_capstyle(dash_capstyle)
        self.set_dash_joinstyle(dash_joinstyle)
        self.set_solid_capstyle(solid_capstyle)
        self.set_solid_joinstyle(solid_joinstyle)

        self._linestyles = None
        self._drawstyle = None
        self._linewidth = linewidth
        self._unscaled_dash_pattern = (0, None)  # offset, dash
        self._dash_pattern = (0, None)  # offset, dash (scaled by linewidth)

        self.set_linewidth(linewidth)
        self.set_linestyle(linestyle)
        self.set_drawstyle(drawstyle)

        self._color = None
        self.set_color(color)
        if marker is None:
            marker = 'none'  # Default.
        if not isinstance(marker, MarkerStyle):
            self._marker = MarkerStyle(marker, fillstyle)
        else:
            self._marker = marker

        self._gapcolor = None
        self.set_gapcolor(gapcolor)

        self._markevery = None
        self._markersize = None
        self._antialiased = None

        self.set_markevery(markevery)
        self.set_antialiased(antialiased)
        self.set_markersize(markersize)

        self._markeredgecolor = None
        self._markeredgewidth = None
        self._markerfacecolor = None
        self._markerfacecoloralt = None

        self.set_markerfacecolor(markerfacecolor)  # Normalizes None to rc.
        self.set_markerfacecoloralt(markerfacecoloralt)
        self.set_markeredgecolor(markeredgecolor)  # Normalizes None to rc.
        self.set_markeredgewidth(markeredgewidth)

        # update kwargs before updating data to give the caller a
        # chance to init axes (and hence unit support)
        self._internal_update(kwargs)
        self.pickradius = pickradius
        self.ind_offset = 0
        if (isinstance(self._picker, Number) and
                not isinstance(self._picker, bool)):
            self._pickradius = self._picker

        self._xorig = np.asarray([])
        self._yorig = np.asarray([])
        self._invalidx = True
        self._invalidy = True
        self._x = None
        self._y = None
        self._xy = None
        self._path = None
        self._transformed_path = None
        self._subslice = False
        self._x_filled = None  # used in subslicing; only x is needed

        self.set_data(xdata, ydata)
