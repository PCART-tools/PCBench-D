    def __init__(self,
                 figsize=None,
                 dpi=None,
                 facecolor=None,
                 edgecolor=None,
                 linewidth=0.0,
                 frameon=None,
                 subplotpars=None,  # default to rc
                 tight_layout=None,  # default to rc figure.autolayout
                 constrained_layout=None,  # default to rc
                                          #figure.constrained_layout.use
                 ):
        """
        Parameters
        ----------
        figsize : 2-tuple of floats, default: :rc:`figure.figsize`
            Figure dimension ``(width, height)`` in inches.

        dpi : float, default: :rc:`figure.dpi`
            Dots per inch.

        facecolor : default: :rc:`figure.facecolor`
            The figure patch facecolor.

        edgecolor : default: :rc:`figure.edgecolor`
            The figure patch edge color.

        linewidth : float
            The linewidth of the frame (i.e. the edge linewidth of the figure
            patch).

        frameon : bool, default: :rc:`figure.frameon`
            If ``False``, suppress drawing the figure frame.

        subplotpars : :class:`SubplotParams`
            Subplot parameters. If not given, the default subplot
            parameters :rc:`figure.subplot.*` are used.

        tight_layout : bool or dict, default: :rc:`figure.autolayout`
            If ``False`` use *subplotpars*. If ``True`` adjust subplot
            parameters using `.tight_layout` with default padding.
            When providing a dict containing the keys ``pad``, ``w_pad``,
            ``h_pad``, and ``rect``, the default `.tight_layout` paddings
            will be overridden.

        constrained_layout : bool
            If ``True`` use constrained layout to adjust positioning of plot
            elements.  Like ``tight_layout``, but designed to be more
            flexible.  See
            :doc:`/tutorials/intermediate/constrainedlayout_guide`
            for examples.  (Note: does not work with :meth:`.subplot` or
            :meth:`.subplot2grid`.)
            Defaults to :rc:`figure.constrained_layout.use`.
        """
        Artist.__init__(self)
        # remove the non-figure artist _axes property
        # as it makes no sense for a figure to be _in_ an axes
        # this is used by the property methods in the artist base class
        # which are over-ridden in this class
        del self._axes
        self.callbacks = cbook.CallbackRegistry()

        if figsize is None:
            figsize = rcParams['figure.figsize']
        if dpi is None:
            dpi = rcParams['figure.dpi']
        if facecolor is None:
            facecolor = rcParams['figure.facecolor']
        if edgecolor is None:
            edgecolor = rcParams['figure.edgecolor']
        if frameon is None:
            frameon = rcParams['figure.frameon']

        if not np.isfinite(figsize).all():
            raise ValueError('figure size must be finite not '
                             '{}'.format(figsize))
        self.bbox_inches = Bbox.from_bounds(0, 0, *figsize)

        self.dpi_scale_trans = Affine2D().scale(dpi, dpi)
        # do not use property as it will trigger
        self._dpi = dpi
        self.bbox = TransformedBbox(self.bbox_inches, self.dpi_scale_trans)

        self.frameon = frameon

        self.transFigure = BboxTransformTo(self.bbox)

        self.patch = Rectangle(
            xy=(0, 0), width=1, height=1,
            facecolor=facecolor, edgecolor=edgecolor, linewidth=linewidth)
        self._set_artist_props(self.patch)
        self.patch.set_aa(False)

        self.canvas = None
        self._suptitle = None

        if subplotpars is None:
            subplotpars = SubplotParams()

        self.subplotpars = subplotpars
        # constrained_layout:
        self._layoutbox = None
        # set in set_constrained_layout_pads()
        self.set_constrained_layout(constrained_layout)

        self.set_tight_layout(tight_layout)

        self._axstack = AxesStack()  # track all figure axes and current axes
        self.clf()
        self._cachedRenderer = None

        # groupers to keep track of x and y labels we want to align.
        # see self.align_xlabels and self.align_ylabels and
        # axis._get_tick_boxes_siblings
        self._align_xlabel_grp = cbook.Grouper()
        self._align_ylabel_grp = cbook.Grouper()

        # list of child gridspecs for this figure
        self._gridspecs = []
