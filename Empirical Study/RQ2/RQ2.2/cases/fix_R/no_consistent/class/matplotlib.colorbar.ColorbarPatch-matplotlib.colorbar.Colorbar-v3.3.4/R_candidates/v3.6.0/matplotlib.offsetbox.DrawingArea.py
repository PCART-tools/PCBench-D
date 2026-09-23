class DrawingArea(OffsetBox):
    """
    The DrawingArea can contain any Artist as a child. The DrawingArea
    has a fixed width and height. The position of children relative to
    the parent is fixed. The children can be clipped at the
    boundaries of the parent.
    """

    def __init__(self, width, height, xdescent=0., ydescent=0., clip=False):
        """
        Parameters
        ----------
        width, height : float
            Width and height of the container box.
        xdescent, ydescent : float
            Descent of the box in x- and y-direction.
        clip : bool
            Whether to clip the children to the box.
        """
        super().__init__()
        self.width = width
        self.height = height
        self.xdescent = xdescent
        self.ydescent = ydescent
        self._clip_children = clip
        self.offset_transform = mtransforms.Affine2D()
        self.dpi_transform = mtransforms.Affine2D()

    @property
    def clip_children(self):
        """
        If the children of this DrawingArea should be clipped
        by DrawingArea bounding box.
        """
        return self._clip_children

    @clip_children.setter
    def clip_children(self, val):
        self._clip_children = bool(val)
        self.stale = True

    def get_transform(self):
        """
        Return the `~matplotlib.transforms.Transform` applied to the children.
        """
        return self.dpi_transform + self.offset_transform

    def set_transform(self, t):
        """
        set_transform is ignored.
        """

    def set_offset(self, xy):
        """
        Set the offset of the container.

        Parameters
        ----------
        xy : (float, float)
            The (x, y) coordinates of the offset in display units.
        """
        self._offset = xy
        self.offset_transform.clear()
        self.offset_transform.translate(xy[0], xy[1])
        self.stale = True

    def get_offset(self):
        """Return offset of the container."""
        return self._offset

    def get_window_extent(self, renderer=None):
        # docstring inherited
        if renderer is None:
            renderer = self.figure._get_renderer()
        w, h, xd, yd = self.get_extent(renderer)
        ox, oy = self.get_offset()  # w, h, xd, yd)

        return mtransforms.Bbox.from_bounds(ox - xd, oy - yd, w, h)

    def get_extent(self, renderer):
        """Return width, height, xdescent, ydescent of box."""
        dpi_cor = renderer.points_to_pixels(1.)
        return (self.width * dpi_cor, self.height * dpi_cor,
                self.xdescent * dpi_cor, self.ydescent * dpi_cor)

    def add_artist(self, a):
        """Add an `.Artist` to the container box."""
        self._children.append(a)
        if not a.is_transform_set():
            a.set_transform(self.get_transform())
        if self.axes is not None:
            a.axes = self.axes
        fig = self.figure
        if fig is not None:
            a.set_figure(fig)

    def draw(self, renderer):
        # docstring inherited

        dpi_cor = renderer.points_to_pixels(1.)
        self.dpi_transform.clear()
        self.dpi_transform.scale(dpi_cor)

        # At this point the DrawingArea has a transform
        # to the display space so the path created is
        # good for clipping children
        tpath = mtransforms.TransformedPath(
            mpath.Path([[0, 0], [0, self.height],
                        [self.width, self.height],
                        [self.width, 0]]),
            self.get_transform())
        for c in self._children:
            if self._clip_children and not (c.clipbox or c._clippath):
                c.set_clip_path(tpath)
            c.draw(renderer)

        bbox_artist(self, renderer, fill=False, props=dict(pad=0.))
        self.stale = False
