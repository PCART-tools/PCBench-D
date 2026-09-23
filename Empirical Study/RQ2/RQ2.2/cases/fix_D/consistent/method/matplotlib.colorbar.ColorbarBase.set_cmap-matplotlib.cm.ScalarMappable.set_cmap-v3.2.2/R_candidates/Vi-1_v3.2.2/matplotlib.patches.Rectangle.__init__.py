    @docstring.dedent_interpd
    def __init__(self, xy, width, height, angle=0.0, **kwargs):
        """
        Parameters
        ----------
        xy : (float, float)
            The bottom and left rectangle coordinates
        width : float
            Rectangle width
        height : float
            Rectangle height
        angle : float, optional
          rotation in degrees anti-clockwise about *xy* (default is 0.0)
        fill : bool, optional
            Whether to fill the rectangle (default is ``True``)

        Notes
        -----
        Valid keyword arguments are:

        %(Patch)s
        """

        Patch.__init__(self, **kwargs)

        self._x0 = xy[0]
        self._y0 = xy[1]

        self._width = width
        self._height = height

        self._x1 = self._x0 + self._width
        self._y1 = self._y0 + self._height

        self.angle = float(angle)
        # Note: This cannot be calculated until this is added to an Axes
        self._rect_transform = transforms.IdentityTransform()
