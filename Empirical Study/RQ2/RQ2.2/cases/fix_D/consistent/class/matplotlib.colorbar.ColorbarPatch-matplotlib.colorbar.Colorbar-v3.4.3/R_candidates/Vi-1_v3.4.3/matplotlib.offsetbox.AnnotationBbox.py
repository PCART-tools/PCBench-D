class AnnotationBbox(martist.Artist, mtext._AnnotationBase):
    """
    Container for an `OffsetBox` referring to a specific position *xy*.

    Optionally an arrow pointing from the offsetbox to *xy* can be drawn.

    This is like `.Annotation`, but with `OffsetBox` instead of `.Text`.
    """

    zorder = 3

    def __str__(self):
        return "AnnotationBbox(%g,%g)" % (self.xy[0], self.xy[1])

    @docstring.dedent_interpd
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
            Whether to draw a frame around the box.

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
        mtext._AnnotationBase.__init__(self,
                                       xy,
                                       xycoords=xycoords,
                                       annotation_clip=annotation_clip)

        self.offsetbox = offsetbox

        self.arrowprops = arrowprops

        self.set_fontsize(fontsize)

        if xybox is None:
            self.xybox = xy
        else:
            self.xybox = xybox

        if boxcoords is None:
            self.boxcoords = xycoords
        else:
            self.boxcoords = boxcoords

        if arrowprops is not None:
            self._arrow_relpos = self.arrowprops.pop("relpos", (0.5, 0.5))
            self.arrow_patch = FancyArrowPatch((0, 0), (1, 1),
                                               **self.arrowprops)
        else:
            self._arrow_relpos = None
            self.arrow_patch = None

        self._box_alignment = box_alignment

        # frame
        self.patch = FancyBboxPatch(
            xy=(0.0, 0.0), width=1., height=1.,
            facecolor='w', edgecolor='k',
            mutation_scale=self.prop.get_size_in_points(),
            snap=True,
            visible=frameon,
        )
        self.patch.set_boxstyle("square", pad=pad)
        if bboxprops:
            self.patch.set(**bboxprops)

        self.update(kwargs)

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
        #if self.arrow_patch is not None:
        #    a, ainfo=self.arrow_patch.contains(event)
        #    t = t or a
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
            s = rcParams["legend.fontsize"]

        self.prop = FontProperties(size=s)
        self.stale = True

    @_api.delete_parameter("3.3", "s")
    def get_fontsize(self, s=None):
        """Return the fontsize in points."""
        return self.prop.get_size_in_points()

    def get_window_extent(self, renderer):
        """
        get the bounding box in display space.
        """
        bboxes = [child.get_window_extent(renderer)
                  for child in self.get_children()]

        return Bbox.union(bboxes)

    def get_tightbbox(self, renderer):
        """
        get tight bounding box in display space.
        """
        bboxes = [child.get_tightbbox(renderer)
                  for child in self.get_children()]

        return Bbox.union(bboxes)

    def update_positions(self, renderer):
        """
        Update the pixel positions of the annotated point and the text.
        """
        xy_pixel = self._get_position_xy(renderer)
        self._update_position_xybox(renderer, xy_pixel)

        mutation_scale = renderer.points_to_pixels(self.get_fontsize())
        self.patch.set_mutation_scale(mutation_scale)

        if self.arrow_patch:
            self.arrow_patch.set_mutation_scale(mutation_scale)

    def _update_position_xybox(self, renderer, xy_pixel):
        """
        Update the pixel positions of the annotation text and the arrow patch.
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

        _fw, _fh = self._box_alignment
        self.offsetbox.set_offset((ox0 - _fw * w + xd, oy0 - _fh * h + yd))

        # update patch position
        bbox = self.offsetbox.get_window_extent(renderer)
        #self.offsetbox.set_offset((ox0-_fw*w, oy0-_fh*h))
        self.patch.set_bounds(bbox.x0, bbox.y0,
                              bbox.width, bbox.height)

        x, y = xy_pixel

        ox1, oy1 = x, y

        if self.arrowprops:
            d = self.arrowprops.copy()

            # Use FancyArrowPatch if self.arrowprops has "arrowstyle" key.

            # adjust the starting point of the arrow relative to
            # the textbox.
            # TODO : Rotation needs to be accounted.
            relpos = self._arrow_relpos

            ox0 = bbox.x0 + bbox.width * relpos[0]
            oy0 = bbox.y0 + bbox.height * relpos[1]

            # The arrow will be drawn from (ox0, oy0) to (ox1,
            # oy1). It will be first clipped by patchA and patchB.
            # Then it will be shrunk by shrinkA and shrinkB
            # (in points). If patch A is not set, self.bbox_patch
            # is used.

            self.arrow_patch.set_positions((ox0, oy0), (ox1, oy1))
            fs = self.prop.get_size_in_points()
            mutation_scale = d.pop("mutation_scale", fs)
            mutation_scale = renderer.points_to_pixels(mutation_scale)
            self.arrow_patch.set_mutation_scale(mutation_scale)

            patchA = d.pop("patchA", self.patch)
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
