class AnnotationBbox(martist.Artist, mtext._AnnotationBase):
    """
    Container for an `OffsetBox` referring to a specific position *xy*.

    Optionally an arrow pointing from the offsetbox to *xy* can be drawn.

    This is like `.Annotation`, but with `OffsetBox` instead of `.Text`.
    """

    zorder = 3

    def __str__(self):
        return "AnnotationBbox(%g,%g)" % (self.xy[0], self.xy[1])

    @_docstring.dedent_interpd
    @_api.make_keyword_only("3.6", name="xycoords")
    def __init__(self, offsetbox, xy,
                 xybox=None,
                 xycoords='data',
                 boxcoords=None,
                 frameon=True, pad=0.4,  # FancyBboxPatch boxstyle.
                 annotation_clip=None,
                 box_alignment=(0.5, 0.5),
                 bboxprops=None,
                 arrowprops=None,
                 fontsize=None,
                 **kwargs):
        """
        Parameters
        ----------
        offsetbox : `OffsetBox`

        xy : (float, float)
            The point *(x, y)* to annotate. The coordinate system is determined
            by *xycoords*.

        xybox : (float, float), default: *xy*
            The position *(x, y)* to place the text at. The coordinate system
            is determined by *boxcoords*.

        xycoords : str or `.Artist` or `.Transform` or callable or \
(float, float), default: 'data'
            The coordinate system that *xy* is given in. See the parameter
            *xycoords* in `.Annotation` for a detailed description.

        boxcoords : str or `.Artist` or `.Transform` or callable or \
(float, float), default: value of *xycoords*
            The coordinate system that *xybox* is given in. See the parameter
            *textcoords* in `.Annotation` for a detailed description.

        frameon : bool, default: True
            By default, the text is surrounded by a white `.FancyBboxPatch`
            (accessible as the ``patch`` attribute of the `.AnnotationBbox`).
            If *frameon* is set to False, this patch is made invisible.

        pad : float, default: 0.4
            Padding around the offsetbox.

        box_alignment : (float, float)
            A tuple of two floats for a vertical and horizontal alignment of
            the offset box w.r.t. the *boxcoords*.
            The lower-left corner is (0, 0) and upper-right corner is (1, 1).

        **kwargs
            Other parameters are identical to `.Annotation`.
        """

        martist.Artist.__init__(self)
        mtext._AnnotationBase.__init__(
            self, xy, xycoords=xycoords, annotation_clip=annotation_clip)

        self.offsetbox = offsetbox
        self.arrowprops = arrowprops.copy() if arrowprops is not None else None
        self.set_fontsize(fontsize)
        self.xybox = xybox if xybox is not None else xy
        self.boxcoords = boxcoords if boxcoords is not None else xycoords
        self._box_alignment = box_alignment

        if arrowprops is not None:
            self._arrow_relpos = self.arrowprops.pop("relpos", (0.5, 0.5))
            self.arrow_patch = FancyArrowPatch((0, 0), (1, 1),
                                               **self.arrowprops)
        else:
            self._arrow_relpos = None
            self.arrow_patch = None

        self.patch = FancyBboxPatch(  # frame
            xy=(0.0, 0.0), width=1., height=1.,
            facecolor='w', edgecolor='k',
            mutation_scale=self.prop.get_size_in_points(),
            snap=True,
            visible=frameon,
        )
        self.patch.set_boxstyle("square", pad=pad)
        if bboxprops:
            self.patch.set(**bboxprops)

        self._internal_update(kwargs)

    @property
    def xyann(self):
        return self.xybox

    @xyann.setter
    def xyann(self, xyann):
        self.xybox = xyann
        self.stale = True

    @property
    def anncoords(self):
        return self.boxcoords

    @anncoords.setter
    def anncoords(self, coords):
        self.boxcoords = coords
        self.stale = True

    def contains(self, mouseevent):
        inside, info = self._default_contains(mouseevent)
        if inside is not None:
            return inside, info
        if not self._check_xy(None):
            return False, {}
        return self.offsetbox.contains(mouseevent)
        # self.arrow_patch is currently not checked as this can be a line - JJ

    def get_children(self):
        children = [self.offsetbox, self.patch]
        if self.arrow_patch:
            children.append(self.arrow_patch)
        return children

    def set_figure(self, fig):
        if self.arrow_patch is not None:
            self.arrow_patch.set_figure(fig)
        self.offsetbox.set_figure(fig)
        martist.Artist.set_figure(self, fig)

    def set_fontsize(self, s=None):
        """
        Set the fontsize in points.

        If *s* is not given, reset to :rc:`legend.fontsize`.
        """
        if s is None:
            s = mpl.rcParams["legend.fontsize"]

        self.prop = FontProperties(size=s)
        self.stale = True

    def get_fontsize(self):
        """Return the fontsize in points."""
        return self.prop.get_size_in_points()

    def get_window_extent(self, renderer=None):
        # docstring inherited
        if renderer is None:
            renderer = self.figure._get_renderer()
        return Bbox.union([child.get_window_extent(renderer)
                           for child in self.get_children()])

    def get_tightbbox(self, renderer=None):
        # docstring inherited
        return Bbox.union([child.get_tightbbox(renderer)
                           for child in self.get_children()])

    def update_positions(self, renderer):
        """
        Update pixel positions for the annotated point, the text and the arrow.
        """

        x, y = self.xybox
        if isinstance(self.boxcoords, tuple):
            xcoord, ycoord = self.boxcoords
            x1, y1 = self._get_xy(renderer, x, y, xcoord)
            x2, y2 = self._get_xy(renderer, x, y, ycoord)
            ox0, oy0 = x1, y2
        else:
            ox0, oy0 = self._get_xy(renderer, x, y, self.boxcoords)

        w, h, xd, yd = self.offsetbox.get_extent(renderer)
        fw, fh = self._box_alignment
        self.offsetbox.set_offset((ox0 - fw * w + xd, oy0 - fh * h + yd))

        bbox = self.offsetbox.get_window_extent(renderer)
        self.patch.set_bounds(bbox.bounds)

        mutation_scale = renderer.points_to_pixels(self.get_fontsize())
        self.patch.set_mutation_scale(mutation_scale)

        if self.arrowprops:
            # Use FancyArrowPatch if self.arrowprops has "arrowstyle" key.

            # Adjust the starting point of the arrow relative to the textbox.
            # TODO: Rotation needs to be accounted.
            arrow_begin = bbox.p0 + bbox.size * self._arrow_relpos
            arrow_end = self._get_position_xy(renderer)
            # The arrow (from arrow_begin to arrow_end) will be first clipped
            # by patchA and patchB, then shrunk by shrinkA and shrinkB (in
            # points).  If patch A is not set, self.bbox_patch is used.
            self.arrow_patch.set_positions(arrow_begin, arrow_end)

            if "mutation_scale" in self.arrowprops:
                mutation_scale = renderer.points_to_pixels(
                    self.arrowprops["mutation_scale"])
                # Else, use fontsize-based mutation_scale defined above.
            self.arrow_patch.set_mutation_scale(mutation_scale)

            patchA = self.arrowprops.get("patchA", self.patch)
            self.arrow_patch.set_patchA(patchA)

    def draw(self, renderer):
        # docstring inherited
        if renderer is not None:
            self._renderer = renderer
        if not self.get_visible() or not self._check_xy(renderer):
            return
        self.update_positions(renderer)
        if self.arrow_patch is not None:
            if self.arrow_patch.figure is None and self.figure is not None:
                self.arrow_patch.figure = self.figure
            self.arrow_patch.draw(renderer)
        self.patch.draw(renderer)
        self.offsetbox.draw(renderer)
        self.stale = False
