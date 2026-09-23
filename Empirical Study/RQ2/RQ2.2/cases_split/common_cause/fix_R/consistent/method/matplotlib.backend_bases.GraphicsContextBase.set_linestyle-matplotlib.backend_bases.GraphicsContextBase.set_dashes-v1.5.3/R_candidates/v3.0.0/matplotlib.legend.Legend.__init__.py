    @docstring.dedent_interpd
    def __init__(self, parent, handles, labels,
                 loc=None,
                 numpoints=None,    # the number of points in the legend line
                 markerscale=None,  # the relative size of legend markers
                                    # vs. original
                 markerfirst=True,  # controls ordering (left-to-right) of
                                    # legend marker and label
                 scatterpoints=None,    # number of scatter points
                 scatteryoffsets=None,
                 prop=None,          # properties for the legend texts
                 fontsize=None,        # keyword to set font size directly

                 # spacing & pad defined as a fraction of the font-size
                 borderpad=None,      # the whitespace inside the legend border
                 labelspacing=None,   # the vertical space between the legend
                                      # entries
                 handlelength=None,   # the length of the legend handles
                 handleheight=None,   # the height of the legend handles
                 handletextpad=None,  # the pad between the legend handle
                                      # and text
                 borderaxespad=None,  # the pad between the axes and legend
                                      # border
                 columnspacing=None,  # spacing between columns

                 ncol=1,     # number of columns
                 mode=None,  # mode for horizontal distribution of columns.
                             # None, "expand"

                 fancybox=None,  # True use a fancy box, false use a rounded
                                 # box, none use rc
                 shadow=None,
                 title=None,  # set a title for the legend
                 title_fontsize=None,  # set to ax.fontsize if None
                 framealpha=None,  # set frame alpha
                 edgecolor=None,  # frame patch edgecolor
                 facecolor=None,  # frame patch facecolor

                 bbox_to_anchor=None,  # bbox that the legend will be anchored.
                 bbox_transform=None,  # transform for the bbox
                 frameon=None,  # draw frame
                 handler_map=None,
                 ):
        """
        Parameters
        ----------
        parent : `~matplotlib.axes.Axes` or `.Figure`
            The artist that contains the legend.

        handles : sequence of `.Artist`
            A list of Artists (lines, patches) to be added to the legend.

        labels : sequence of strings
            A list of labels to show next to the artists. The length of handles
            and labels should be the same. If they are not, they are truncated
            to the smaller of both lengths.

        Other Parameters
        ----------------

        %(_legend_kw_doc)s

        Notes
        -----

        Users can specify any arbitrary location for the legend using the
        *bbox_to_anchor* keyword argument. bbox_to_anchor can be an instance
        of BboxBase(or its derivatives) or a tuple of 2 or 4 floats.
        See :meth:`set_bbox_to_anchor` for more detail.

        The legend location can be specified by setting *loc* with a tuple of
        2 floats, which is interpreted as the lower-left corner of the legend
        in the normalized axes coordinate.
        """
        # local import only to avoid circularity
        from matplotlib.axes import Axes
        from matplotlib.figure import Figure

        Artist.__init__(self)

        if prop is None:
            if fontsize is not None:
                self.prop = FontProperties(size=fontsize)
            else:
                self.prop = FontProperties(size=rcParams["legend.fontsize"])
        elif isinstance(prop, dict):
            self.prop = FontProperties(**prop)
            if "size" not in prop:
                self.prop.set_size(rcParams["legend.fontsize"])
        else:
            self.prop = prop

        self._fontsize = self.prop.get_size_in_points()

        self.texts = []
        self.legendHandles = []
        self._legend_title_box = None

        #: A dictionary with the extra handler mappings for this Legend
        #: instance.
        self._custom_handler_map = handler_map

        locals_view = locals()
        for name in ["numpoints", "markerscale", "shadow", "columnspacing",
                     "scatterpoints", "handleheight", 'borderpad',
                     'labelspacing', 'handlelength', 'handletextpad',
                     'borderaxespad']:
            if locals_view[name] is None:
                value = rcParams["legend." + name]
            else:
                value = locals_view[name]
            setattr(self, name, value)
        del locals_view
        # trim handles and labels if illegal label...
        _lab, _hand = [], []
        for label, handle in zip(labels, handles):
            if isinstance(label, str) and label.startswith('_'):
                warnings.warn('The handle {!r} has a label of {!r} which '
                              'cannot be automatically added to the '
                              'legend.'.format(handle, label))
            else:
                _lab.append(label)
                _hand.append(handle)
        labels, handles = _lab, _hand

        handles = list(handles)
        if len(handles) < 2:
            ncol = 1
        self._ncol = ncol

        if self.numpoints <= 0:
            raise ValueError("numpoints must be > 0; it was %d" % numpoints)

        # introduce y-offset for handles of the scatter plot
        if scatteryoffsets is None:
            self._scatteryoffsets = np.array([3. / 8., 4. / 8., 2.5 / 8.])
        else:
            self._scatteryoffsets = np.asarray(scatteryoffsets)
        reps = self.scatterpoints // len(self._scatteryoffsets) + 1
        self._scatteryoffsets = np.tile(self._scatteryoffsets,
                                        reps)[:self.scatterpoints]

        # _legend_box is an OffsetBox instance that contains all
        # legend items and will be initialized from _init_legend_box()
        # method.
        self._legend_box = None

        if isinstance(parent, Axes):
            self.isaxes = True
            self.axes = parent
            self.set_figure(parent.figure)
        elif isinstance(parent, Figure):
            self.isaxes = False
            self.set_figure(parent)
        else:
            raise TypeError("Legend needs either Axes or Figure as parent")
        self.parent = parent

        if loc is None:
            loc = rcParams["legend.loc"]
            if not self.isaxes and loc in [0, 'best']:
                loc = 'upper right'
        if isinstance(loc, str):
            if loc not in self.codes:
                if self.isaxes:
                    warnings.warn('Unrecognized location "%s". Falling back '
                                  'on "best"; valid locations are\n\t%s\n'
                                  % (loc, '\n\t'.join(self.codes)))
                    loc = 0
                else:
                    warnings.warn('Unrecognized location "%s". Falling back '
                                  'on "upper right"; '
                                  'valid locations are\n\t%s\n'
                                  % (loc, '\n\t'.join(self.codes)))
                    loc = 1
            else:
                loc = self.codes[loc]
        if not self.isaxes and loc == 0:
            warnings.warn('Automatic legend placement (loc="best") not '
                          'implemented for figure legend. '
                          'Falling back on "upper right".')
            loc = 1

        self._mode = mode
        self.set_bbox_to_anchor(bbox_to_anchor, bbox_transform)

        # We use FancyBboxPatch to draw a legend frame. The location
        # and size of the box will be updated during the drawing time.

        if facecolor is None:
            facecolor = rcParams["legend.facecolor"]
        if facecolor == 'inherit':
            facecolor = rcParams["axes.facecolor"]

        if edgecolor is None:
            edgecolor = rcParams["legend.edgecolor"]
        if edgecolor == 'inherit':
            edgecolor = rcParams["axes.edgecolor"]

        self.legendPatch = FancyBboxPatch(
            xy=(0.0, 0.0), width=1., height=1.,
            facecolor=facecolor,
            edgecolor=edgecolor,
            mutation_scale=self._fontsize,
            snap=True
            )

        # The width and height of the legendPatch will be set (in the
        # draw()) to the length that includes the padding. Thus we set
        # pad=0 here.
        if fancybox is None:
            fancybox = rcParams["legend.fancybox"]

        if fancybox:
            self.legendPatch.set_boxstyle("round", pad=0,
                                          rounding_size=0.2)
        else:
            self.legendPatch.set_boxstyle("square", pad=0)

        self._set_artist_props(self.legendPatch)

        self._drawFrame = frameon
        if frameon is None:
            self._drawFrame = rcParams["legend.frameon"]

        # init with null renderer
        self._init_legend_box(handles, labels, markerfirst)

        # If shadow is activated use framealpha if not
        # explicitly passed. See Issue 8943
        if framealpha is None:
            if shadow:
                self.get_frame().set_alpha(1)
            else:
                self.get_frame().set_alpha(rcParams["legend.framealpha"])
        else:
            self.get_frame().set_alpha(framealpha)

        self._loc = loc
        # figure out title fontsize:
        if title_fontsize is None:
            title_fontsize = rcParams['legend.title_fontsize']
        tprop = FontProperties(size=title_fontsize)
        self.set_title(title, prop=tprop)
        self._last_fontsize_points = self._fontsize
        self._draggable = None
