class AuxTransformBox(OffsetBox):
    """
    Offset Box with the aux_transform. Its children will be
    transformed with the aux_transform first then will be
    offsetted. The absolute coordinate of the aux_transform is meaning
    as it will be automatically adjust so that the left-lower corner
    of the bounding box of children will be set to (0, 0) before the
    offset transform.

    It is similar to drawing area, except that the extent of the box
    is not predetermined but calculated from the window extent of its
    children. Furthermore, the extent of the children will be
    calculated in the transformed coordinate.
    """
    def __init__(self, aux_transform):
        self.aux_transform = aux_transform
        super().__init__()
        self.offset_transform = mtransforms.Affine2D()
        # ref_offset_transform makes offset_transform always relative to the
        # lower-left corner of the bbox of its children.
        self.ref_offset_transform = mtransforms.Affine2D()

    def add_artist(self, a):
        """Add an `.Artist` to the container box."""
        self._children.append(a)
        a.set_transform(self.get_transform())
        self.stale = True

    def get_transform(self):
        """
        Return the :class:`~matplotlib.transforms.Transform` applied
        to the children
        """
        return (self.aux_transform
                + self.ref_offset_transform
                + self.offset_transform)

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

    def get_window_extent(self, renderer):
        """Return the bounding box in display space."""
        w, h, xd, yd = self.get_extent(renderer)
        ox, oy = self.get_offset()  # w, h, xd, yd)
        return mtransforms.Bbox.from_bounds(ox - xd, oy - yd, w, h)

    def get_extent(self, renderer):
        # clear the offset transforms
        _off = self.offset_transform.get_matrix()  # to be restored later
        self.ref_offset_transform.clear()
        self.offset_transform.clear()
        # calculate the extent
        bboxes = [c.get_window_extent(renderer) for c in self._children]
        ub = mtransforms.Bbox.union(bboxes)
        # adjust ref_offset_transform
        self.ref_offset_transform.translate(-ub.x0, -ub.y0)
        # restore offset transform
        self.offset_transform.set_matrix(_off)

        return ub.width, ub.height, 0., 0.

    def draw(self, renderer):
        # docstring inherited
        for c in self._children:
            c.draw(renderer)
        bbox_artist(self, renderer, fill=False, props=dict(pad=0.))
        self.stale = False
