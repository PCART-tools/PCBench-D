    def __init__(self, xdata, ydata,
                 linewidth=None,  # all Nones default to rc
                 linestyle=None,
                 color=None,
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

        %(_Line2D_docstr)s

        See :meth:`set_linestyle` for a description of the line styles,
        :meth:`set_marker` for a description of the markers, and
        :meth:`set_drawstyle` for a description of the draw styles.

        """
        Artist.__init__(self)

        #convert sequences to numpy arrays
        if not np.iterable(xdata):
            raise RuntimeError('xdata must be a sequence')
        if not np.iterable(ydata):
            raise RuntimeError('ydata must be a sequence')

        if linewidth is None:
            linewidth = rcParams['lines.linewidth']

        if linestyle is None:
            linestyle = rcParams['lines.linestyle']
        if marker is None:
            marker = rcParams['lines.marker']
        if markerfacecolor is None:
            markerfacecolor = rcParams['lines.markerfacecolor']
        if markeredgecolor is None:
            markeredgecolor = rcParams['lines.markeredgecolor']
        if color is None:
            color = rcParams['lines.color']

        if markersize is None:
            markersize = rcParams['lines.markersize']
        if antialiased is None:
            antialiased = rcParams['lines.antialiased']
        if dash_capstyle is None:
            dash_capstyle = rcParams['lines.dash_capstyle']
        if dash_joinstyle is None:
            dash_joinstyle = rcParams['lines.dash_joinstyle']
        if solid_capstyle is None:
            solid_capstyle = rcParams['lines.solid_capstyle']
        if solid_joinstyle is None:
            solid_joinstyle = rcParams['lines.solid_joinstyle']

        if isinstance(linestyle, str):
            ds, ls = self._split_drawstyle_linestyle(linestyle)
            if ds is not None and drawstyle is not None and ds != drawstyle:
                raise ValueError("Inconsistent drawstyle ({!r}) and linestyle "
                                 "({!r})".format(drawstyle, linestyle))
            linestyle = ls

            if ds is not None:
                drawstyle = ds

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

        # scaled dash + offset
        self._dashSeq = None
        self._dashOffset = 0
        # unscaled dash + offset
        # this is needed scaling the dash pattern by linewidth
        self._us_dashSeq = None
        self._us_dashOffset = 0

        self.set_linewidth(linewidth)
        self.set_linestyle(linestyle)
        self.set_drawstyle(drawstyle)

        self._color = None
        self.set_color(color)
        self._marker = MarkerStyle(marker, fillstyle)

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

        self.set_markerfacecolor(markerfacecolor)
        self.set_markerfacecoloralt(markerfacecoloralt)
        self.set_markeredgecolor(markeredgecolor)
        self.set_markeredgewidth(markeredgewidth)

        # update kwargs before updating data to give the caller a
        # chance to init axes (and hence unit support)
        self.update(kwargs)
        self.pickradius = pickradius
        self.ind_offset = 0
        if isinstance(self._picker, Number):
            self.pickradius = self._picker

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
