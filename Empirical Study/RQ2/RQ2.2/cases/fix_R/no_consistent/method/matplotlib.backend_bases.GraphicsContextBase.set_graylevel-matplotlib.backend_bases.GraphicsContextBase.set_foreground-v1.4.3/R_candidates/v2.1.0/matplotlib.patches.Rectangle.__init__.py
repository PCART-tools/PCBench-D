    @docstring.dedent_interpd
    def __init__(self, xy, width, height, angle=0.0, **kwargs):
        """

        *angle*
          rotation in degrees (anti-clockwise)

        *fill* is a boolean indicating whether to fill the rectangle

        Valid kwargs are:
        %(Patch)s
        """

        Patch.__init__(self, **kwargs)

        self._x = xy[0]
        self._y = xy[1]
        self._width = width
        self._height = height
        self.angle = float(angle)
        # Note: This cannot be calculated until this is added to an Axes
        self._rect_transform = transforms.IdentityTransform()
