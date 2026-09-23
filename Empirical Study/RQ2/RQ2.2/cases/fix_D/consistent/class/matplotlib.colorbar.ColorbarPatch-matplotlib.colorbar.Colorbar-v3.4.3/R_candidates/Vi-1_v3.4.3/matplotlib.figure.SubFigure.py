class SubFigure(FigureBase):
    """
    Logical figure that can be placed inside a figure.

    Typically instantiated using `.Figure.add_subfigure` or
    `.SubFigure.add_subfigure`, or `.SubFigure.subfigures`.  A subfigure has
    the same methods as a figure except for those particularly tied to the size
    or dpi of the figure, and is confined to a prescribed region of the figure.
    For example the following puts two subfigures side-by-side::

        fig = plt.figure()
        sfigs = fig.subfigures(1, 2)
        axsL = sfigs[0].subplots(1, 2)
        axsR = sfigs[1].subplots(2, 1)

    See :doc:`/gallery/subplots_axes_and_figures/subfigures`
    """

    def __init__(self, parent, subplotspec, *,
                 facecolor=None,
                 edgecolor=None,
                 linewidth=0.0,
                 frameon=None):
        """
        Parameters
        ----------
        parent : `.figure.Figure` or `.figure.SubFigure`
            Figure or subfigure that contains the SubFigure.  SubFigures
            can be nested.

        subplotspec : `.gridspec.SubplotSpec`
            Defines the region in a parent gridspec where the subfigure will
            be placed.

        facecolor : default: :rc:`figure.facecolor`
            The figure patch face color.

        edgecolor : default: :rc:`figure.edgecolor`
            The figure patch edge color.

        linewidth : float
            The linewidth of the frame (i.e. the edge linewidth of the figure
            patch).

        frameon : bool, default: :rc:`figure.frameon`
            If ``False``, suppress drawing the figure background patch.
        """
        super().__init__()
        if facecolor is None:
            facecolor = mpl.rcParams['figure.facecolor']
        if edgecolor is None:
            edgecolor = mpl.rcParams['figure.edgecolor']
        if frameon is None:
            frameon = mpl.rcParams['figure.frameon']

        self._subplotspec = subplotspec
        self._parent = parent
        self.figure = parent.figure
        # subfigures use the parent axstack
        self._axstack = parent._axstack
        self.subplotpars = parent.subplotpars
        self.dpi_scale_trans = parent.dpi_scale_trans
        self._axobservers = parent._axobservers
        self.canvas = parent.canvas
        self.transFigure = parent.transFigure
        self.bbox_relative = None
        self._redo_transform_rel_fig()
        self.figbbox = self._parent.figbbox
        self.bbox = TransformedBbox(self.bbox_relative,
                                    self._parent.transSubfigure)
        self.transSubfigure = BboxTransformTo(self.bbox)

        self.patch = Rectangle(
            xy=(0, 0), width=1, height=1, visible=frameon,
            facecolor=facecolor, edgecolor=edgecolor, linewidth=linewidth,
            # Don't let the figure patch influence bbox calculation.
            in_layout=False, transform=self.transSubfigure)
        self._set_artist_props(self.patch)
        self.patch.set_antialiased(False)

        if parent._layoutgrid is not None:
            self.init_layoutgrid()

    @property
    def dpi(self):
        return self._parent.dpi

    @dpi.setter
    def dpi(self, value):
        self._parent.dpi = value

    def _redo_transform_rel_fig(self, bbox=None):
        """
        Make the transSubfigure bbox relative to Figure transform.

        Parameters
        ----------
        bbox : bbox or None
            If not None, then the bbox is used for relative bounding box.
            Otherwise it is calculated from the subplotspec.
        """

        if bbox is not None:
            self.bbox_relative.p0 = bbox.p0
            self.bbox_relative.p1 = bbox.p1
            return

        gs = self._subplotspec.get_gridspec()
        # need to figure out *where* this subplotspec is.
        wr = gs.get_width_ratios()
        hr = gs.get_height_ratios()
        nrows, ncols = gs.get_geometry()
        if wr is None:
            wr = np.ones(ncols)
        else:
            wr = np.array(wr)
        if hr is None:
            hr = np.ones(nrows)
        else:
            hr = np.array(hr)
        widthf = np.sum(wr[self._subplotspec.colspan]) / np.sum(wr)
        heightf = np.sum(hr[self._subplotspec.rowspan]) / np.sum(hr)

        x0 = 0
        if not self._subplotspec.is_first_col():
            x0 += np.sum(wr[:self._subplotspec.colspan.start]) / np.sum(wr)

        y0 = 0
        if not self._subplotspec.is_last_row():
            y0 += 1 - (np.sum(hr[:self._subplotspec.rowspan.stop]) /
                       np.sum(hr))

        if self.bbox_relative is None:
            self.bbox_relative = Bbox.from_bounds(x0, y0, widthf, heightf)
        else:
            self.bbox_relative.p0 = (x0, y0)
            self.bbox_relative.p1 = (x0 + widthf, y0 + heightf)

    def get_constrained_layout(self):
        """
        Return whether constrained layout is being used.

        See :doc:`/tutorials/intermediate/constrainedlayout_guide`.
        """
        return self._parent.get_constrained_layout()

    def get_constrained_layout_pads(self, relative=False):
        """
        Get padding for ``constrained_layout``.

        Returns a list of ``w_pad, h_pad`` in inches and
        ``wspace`` and ``hspace`` as fractions of the subplot.

        See :doc:`/tutorials/intermediate/constrainedlayout_guide`.

        Parameters
        ----------
        relative : bool
            If `True`, then convert from inches to figure relative.
        """
        return self._parent.get_constrained_layout_pads(relative=relative)

    def init_layoutgrid(self):
        """Initialize the layoutgrid for use in constrained_layout."""
        if self._layoutgrid is None:
            gs = self._subplotspec.get_gridspec()
            parent = gs._layoutgrid
            if parent is not None:
                self._layoutgrid = layoutgrid.LayoutGrid(
                    parent=parent,
                    name=(parent.name + '.' + 'panellb' +
                          layoutgrid.seq_id()),
                    parent_inner=True,
                    nrows=1, ncols=1,
                    parent_pos=(self._subplotspec.rowspan,
                                self._subplotspec.colspan))

    def get_axes(self):
        """
        Return a list of Axes in the SubFigure. You can access and modify the
        Axes in the Figure through this list.

        Do not modify the list itself. Instead, use `~.SubFigure.add_axes`,
        `~.SubFigure.add_subplot` or `~.SubFigure.delaxes` to add or remove an
        Axes.

        Note: This is equivalent to the property `~.SubFigure.axes`.
        """
        return self._localaxes.as_list()

    axes = property(get_axes, doc="""
        List of Axes in the SubFigure.  You can access and modify the Axes
        in the SubFigure through this list.

        Do not modify the list itself. Instead, use `~.SubFigure.add_axes`,
        `~.SubFigure.add_subplot` or `~.SubFigure.delaxes` to add or remove an
        Axes.
        """)

    def draw(self, renderer):
        # docstring inherited
        self._cachedRenderer = renderer

        # draw the figure bounding box, perhaps none for white figure
        if not self.get_visible():
            return

        artists = self._get_draw_artists(renderer)

        try:
            renderer.open_group('subfigure', gid=self.get_gid())
            self.patch.draw(renderer)
            mimage._draw_list_compositing_images(renderer, self, artists)
            for sfig in self.subfigs:
                sfig.draw(renderer)
            renderer.close_group('subfigure')

        finally:
            self.stale = False
