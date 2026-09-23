class Tick(martist.Artist):
    """
    Abstract base class for the axis ticks, grid lines and labels.

    Ticks mark a position on an Axis. They contain two lines as markers and
    two labels; one each for the bottom and top positions (in case of an
    `.XAxis`) or for the left and right positions (in case of a `.YAxis`).

    Attributes
    ----------
    tick1line : `.Line2D`
        The left/bottom tick marker.
    tick2line : `.Line2D`
        The right/top tick marker.
    gridline : `.Line2D`
        The grid line associated with the label position.
    label1 : `.Text`
        The left/bottom tick label.
    label2 : `.Text`
        The right/top tick label.

    """
    def __init__(self, axes, loc, *,
                 size=None,  # points
                 width=None,
                 color=None,
                 tickdir=None,
                 pad=None,
                 labelsize=None,
                 labelcolor=None,
                 zorder=None,
                 gridOn=None,  # defaults to axes.grid depending on
                               # axes.grid.which
                 tick1On=True,
                 tick2On=True,
                 label1On=True,
                 label2On=False,
                 major=True,
                 labelrotation=0,
                 grid_color=None,
                 grid_linestyle=None,
                 grid_linewidth=None,
                 grid_alpha=None,
                 **kw  # Other Line2D kwargs applied to gridlines.
                 ):
        """
        bbox is the Bound2D bounding box in display coords of the Axes
        loc is the tick location in data coords
        size is the tick size in points
        """
        super().__init__()

        if gridOn is None:
            if major and (mpl.rcParams['axes.grid.which']
                          in ('both', 'major')):
                gridOn = mpl.rcParams['axes.grid']
            elif (not major) and (mpl.rcParams['axes.grid.which']
                                  in ('both', 'minor')):
                gridOn = mpl.rcParams['axes.grid']
            else:
                gridOn = False

        self.set_figure(axes.figure)
        self.axes = axes

        self._loc = loc
        self._major = major

        name = self.__name__
        major_minor = "major" if major else "minor"

        if size is None:
            size = mpl.rcParams[f"{name}.{major_minor}.size"]
        self._size = size

        if width is None:
            width = mpl.rcParams[f"{name}.{major_minor}.width"]
        self._width = width

        if color is None:
            color = mpl.rcParams[f"{name}.color"]

        if pad is None:
            pad = mpl.rcParams[f"{name}.{major_minor}.pad"]
        self._base_pad = pad

        if labelcolor is None:
            labelcolor = mpl.rcParams[f"{name}.labelcolor"]

        if labelcolor == 'inherit':
            # inherit from tick color
            labelcolor = mpl.rcParams[f"{name}.color"]

        if labelsize is None:
            labelsize = mpl.rcParams[f"{name}.labelsize"]

        self._set_labelrotation(labelrotation)

        if zorder is None:
            if major:
                zorder = mlines.Line2D.zorder + 0.01
            else:
                zorder = mlines.Line2D.zorder
        self._zorder = zorder

        if grid_color is None:
            grid_color = mpl.rcParams["grid.color"]
        if grid_linestyle is None:
            grid_linestyle = mpl.rcParams["grid.linestyle"]
        if grid_linewidth is None:
            grid_linewidth = mpl.rcParams["grid.linewidth"]
        if grid_alpha is None:
            grid_alpha = mpl.rcParams["grid.alpha"]
        grid_kw = {k[5:]: v for k, v in kw.items()}

        self.tick1line = mlines.Line2D(
            [], [],
            color=color, linestyle="none", zorder=zorder, visible=tick1On,
            markeredgecolor=color, markersize=size, markeredgewidth=width,
        )
        self.tick2line = mlines.Line2D(
            [], [],
            color=color, linestyle="none", zorder=zorder, visible=tick2On,
            markeredgecolor=color, markersize=size, markeredgewidth=width,
        )
        self.gridline = mlines.Line2D(
            [], [],
            color=grid_color, alpha=grid_alpha, visible=gridOn,
            linestyle=grid_linestyle, linewidth=grid_linewidth, marker="",
            **grid_kw,
        )
        self.gridline.get_path()._interpolation_steps = \
            GRIDLINE_INTERPOLATION_STEPS
        self.label1 = mtext.Text(
            np.nan, np.nan,
            fontsize=labelsize, color=labelcolor, visible=label1On,
            rotation=self._labelrotation[1])
        self.label2 = mtext.Text(
            np.nan, np.nan,
            fontsize=labelsize, color=labelcolor, visible=label2On,
            rotation=self._labelrotation[1])

        self._apply_tickdir(tickdir)

        for artist in [self.tick1line, self.tick2line, self.gridline,
                       self.label1, self.label2]:
            self._set_artist_props(artist)

        self.update_position(loc)

    @property
    @_api.deprecated("3.1", alternative="Tick.label1", pending=True)
    def label(self):
        return self.label1

    def _set_labelrotation(self, labelrotation):
        if isinstance(labelrotation, str):
            mode = labelrotation
            angle = 0
        elif isinstance(labelrotation, (tuple, list)):
            mode, angle = labelrotation
        else:
            mode = 'default'
            angle = labelrotation
        _api.check_in_list(['auto', 'default'], labelrotation=mode)
        self._labelrotation = (mode, angle)

    def _apply_tickdir(self, tickdir):
        """Set tick direction.  Valid values are 'out', 'in', 'inout'."""
        # This method is responsible for updating `_pad`, and, in subclasses,
        # for setting the tick{1,2}line markers as well.  From the user
        # perspective this should always be called though _apply_params, which
        # further updates ticklabel positions using the new pads.
        if tickdir is None:
            tickdir = mpl.rcParams[f'{self.__name__}.direction']
        _api.check_in_list(['in', 'out', 'inout'], tickdir=tickdir)
        self._tickdir = tickdir
        self._pad = self._base_pad + self.get_tick_padding()

    @_api.deprecated("3.5", alternative="axis.set_tick_params")
    def apply_tickdir(self, tickdir):
        self._apply_tickdir(tickdir)
        self.stale = True

    def get_tickdir(self):
        return self._tickdir

    def get_tick_padding(self):
        """Get the length of the tick outside of the axes."""
        padding = {
            'in': 0.0,
            'inout': 0.5,
            'out': 1.0
        }
        return self._size * padding[self._tickdir]

    def get_children(self):
        children = [self.tick1line, self.tick2line,
                    self.gridline, self.label1, self.label2]
        return children

    def set_clip_path(self, clippath, transform=None):
        # docstring inherited
        super().set_clip_path(clippath, transform)
        self.gridline.set_clip_path(clippath, transform)
        self.stale = True

    def get_pad_pixels(self):
        return self.figure.dpi * self._base_pad / 72

    def contains(self, mouseevent):
        """
        Test whether the mouse event occurred in the Tick marks.

        This function always returns false.  It is more useful to test if the
        axis as a whole contains the mouse rather than the set of tick marks.
        """
        inside, info = self._default_contains(mouseevent)
        if inside is not None:
            return inside, info
        return False, {}

    def set_pad(self, val):
        """
        Set the tick label pad in points

        Parameters
        ----------
        val : float
        """
        self._apply_params(pad=val)
        self.stale = True

    def get_pad(self):
        """Get the value of the tick label pad in points."""
        return self._base_pad

    def _get_text1(self):
        """Get the default Text 1 instance."""

    def _get_text2(self):
        """Get the default Text 2 instance."""

    def _get_tick1line(self):
        """Get the default line2D instance for tick1."""

    def _get_tick2line(self):
        """Get the default line2D instance for tick2."""

    def _get_gridline(self):
        """Get the default grid Line2d instance for this tick."""

    def get_loc(self):
        """Return the tick location (data coords) as a scalar."""
        return self._loc

    @martist.allow_rasterization
    def draw(self, renderer):
        if not self.get_visible():
            self.stale = False
            return
        renderer.open_group(self.__name__, gid=self.get_gid())
        for artist in [self.gridline, self.tick1line, self.tick2line,
                       self.label1, self.label2]:
            artist.draw(renderer)
        renderer.close_group(self.__name__)
        self.stale = False

    def set_label1(self, s):
        """
        Set the label1 text.

        Parameters
        ----------
        s : str
        """
        self.label1.set_text(s)
        self.stale = True

    set_label = set_label1

    def set_label2(self, s):
        """
        Set the label2 text.

        Parameters
        ----------
        s : str
        """
        self.label2.set_text(s)
        self.stale = True

    def set_url(self, url):
        """
        Set the url of label1 and label2.

        Parameters
        ----------
        url : str
        """
        super().set_url(url)
        self.label1.set_url(url)
        self.label2.set_url(url)
        self.stale = True

    def _set_artist_props(self, a):
        a.set_figure(self.figure)

    def get_view_interval(self):
        """
        Return the view limits ``(min, max)`` of the axis the tick belongs to.
        """
        raise NotImplementedError('Derived must override')

    def _apply_params(self, **kw):
        for name, target in [("gridOn", self.gridline),
                             ("tick1On", self.tick1line),
                             ("tick2On", self.tick2line),
                             ("label1On", self.label1),
                             ("label2On", self.label2)]:
            if name in kw:
                target.set_visible(kw.pop(name))
        if any(k in kw for k in ['size', 'width', 'pad', 'tickdir']):
            self._size = kw.pop('size', self._size)
            # Width could be handled outside this block, but it is
            # convenient to leave it here.
            self._width = kw.pop('width', self._width)
            self._base_pad = kw.pop('pad', self._base_pad)
            # _apply_tickdir uses _size and _base_pad to make _pad, and also
            # sets the ticklines markers.
            self._apply_tickdir(kw.pop('tickdir', self._tickdir))
            for line in (self.tick1line, self.tick2line):
                line.set_markersize(self._size)
                line.set_markeredgewidth(self._width)
            # _get_text1_transform uses _pad from _apply_tickdir.
            trans = self._get_text1_transform()[0]
            self.label1.set_transform(trans)
            trans = self._get_text2_transform()[0]
            self.label2.set_transform(trans)
        tick_kw = {k: v for k, v in kw.items() if k in ['color', 'zorder']}
        if 'color' in kw:
            tick_kw['markeredgecolor'] = kw['color']
        self.tick1line.set(**tick_kw)
        self.tick2line.set(**tick_kw)
        for k, v in tick_kw.items():
            setattr(self, '_' + k, v)

        if 'labelrotation' in kw:
            self._set_labelrotation(kw.pop('labelrotation'))
            self.label1.set(rotation=self._labelrotation[1])
            self.label2.set(rotation=self._labelrotation[1])

        label_kw = {k[5:]: v for k, v in kw.items()
                    if k in ['labelsize', 'labelcolor']}
        self.label1.set(**label_kw)
        self.label2.set(**label_kw)

        grid_kw = {k[5:]: v for k, v in kw.items()
                   if k in _gridline_param_names}
        self.gridline.set(**grid_kw)

    def update_position(self, loc):
        """Set the location of tick in data coords with scalar *loc*."""
        raise NotImplementedError('Derived must override')

    def _get_text1_transform(self):
        raise NotImplementedError('Derived must override')

    def _get_text2_transform(self):
        raise NotImplementedError('Derived must override')
