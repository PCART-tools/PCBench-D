    def __init__(self,
                 figsize=None,  # defaults to rc figure.figsize
                 dpi=None,  # defaults to rc figure.dpi
                 facecolor=None,  # defaults to rc figure.facecolor
                 edgecolor=None,  # defaults to rc figure.edgecolor
                 linewidth=0.0,  # the default linewidth of the frame
                 frameon=None,  # whether or not to draw the figure frame
                 subplotpars=None,  # default to rc
                 tight_layout=None,  # default to rc figure.autolayout
                 ):
        """
        *figsize*
            w,h tuple in inches

        *dpi*
            Dots per inch

        *facecolor*
            The figure patch facecolor; defaults to rc ``figure.facecolor``

        *edgecolor*
            The figure patch edge color; defaults to rc ``figure.edgecolor``

        *linewidth*
            The figure patch edge linewidth; the default linewidth of the frame

        *frameon*
            If *False*, suppress drawing the figure frame

        *subplotpars*
            A :class:`SubplotParams` instance, defaults to rc

        *tight_layout*
            If *False* use *subplotpars*; if *True* adjust subplot
            parameters using :meth:`tight_layout` with default padding.
            When providing a dict containing the keys `pad`, `w_pad`, `h_pad`
            and `rect`, the default :meth:`tight_layout` paddings will be
            overridden.
            Defaults to rc ``figure.autolayout``.
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

        self._hold = rcParams['axes.hold']
        if self._hold is None:
            self._hold = True

        self.canvas = None
        self._suptitle = None

        if subplotpars is None:
            subplotpars = SubplotParams()

        self.subplotpars = subplotpars
        self.set_tight_layout(tight_layout)

        self._axstack = AxesStack()  # track all figure axes and current axes
        self.clf()
        self._cachedRenderer = None
