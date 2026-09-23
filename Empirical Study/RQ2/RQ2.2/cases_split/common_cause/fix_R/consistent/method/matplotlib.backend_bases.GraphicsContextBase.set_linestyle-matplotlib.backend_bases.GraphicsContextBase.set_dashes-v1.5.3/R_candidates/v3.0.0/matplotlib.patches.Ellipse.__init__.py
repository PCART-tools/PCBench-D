    @docstring.dedent_interpd
    def __init__(self, xy, width, height, angle=0, **kwargs):
        """
        Parameters
        ----------
        xy : tuple of (scalar, scalar)
            xy coordinates of ellipse centre.
        width : scalar
            Total length (diameter) of horizontal axis.
        height : scalar
            Total length (diameter) of vertical axis.
        angle : scalar, optional
            Rotation in degrees anti-clockwise.

        Notes
        -----
        Valid keyword arguments are
        %(Patch)s
        """
        Patch.__init__(self, **kwargs)

        self._center = xy
        self.width, self.height = width, height
        self.angle = angle
        self._path = Path.unit_circle()
        # Note: This cannot be calculated until this is added to an Axes
        self._patch_transform = transforms.IdentityTransform()
