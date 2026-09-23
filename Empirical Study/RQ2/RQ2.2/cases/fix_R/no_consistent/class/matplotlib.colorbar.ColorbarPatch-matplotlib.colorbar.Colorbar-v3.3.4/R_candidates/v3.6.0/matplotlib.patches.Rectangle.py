class Rectangle(Patch):
    """
    A rectangle defined via an anchor point *xy* and its *width* and *height*.

    The rectangle extends from ``xy[0]`` to ``xy[0] + width`` in x-direction
    and from ``xy[1]`` to ``xy[1] + height`` in y-direction. ::

      :                +------------------+
      :                |                  |
      :              height               |
      :                |                  |
      :               (xy)---- width -----+

    One may picture *xy* as the bottom left corner, but which corner *xy* is
    actually depends on the direction of the axis and the sign of *width*
    and *height*; e.g. *xy* would be the bottom right corner if the x-axis
    was inverted or if *width* was negative.
    """

    def __str__(self):
        pars = self._x0, self._y0, self._width, self._height, self.angle
        fmt = "Rectangle(xy=(%g, %g), width=%g, height=%g, angle=%g)"
        return fmt % pars

    @_docstring.dedent_interpd
    @_api.make_keyword_only("3.6", name="angle")
    def __init__(self, xy, width, height, angle=0.0, *,
                 rotation_point='xy', **kwargs):
        """
        Parameters
        ----------
        xy : (float, float)
            The anchor point.
        width : float
            Rectangle width.
        height : float
            Rectangle height.
        angle : float, default: 0
            Rotation in degrees anti-clockwise about the rotation point.
        rotation_point : {'xy', 'center', (number, number)}, default: 'xy'
            If ``'xy'``, rotate around the anchor point. If ``'center'`` rotate
            around the center. If 2-tuple of number, rotate around this
            coordinate.

        Other Parameters
        ----------------
        **kwargs : `.Patch` properties
            %(Patch:kwdoc)s
        """
        super().__init__(**kwargs)
        self._x0 = xy[0]
        self._y0 = xy[1]
        self._width = width
        self._height = height
        self.angle = float(angle)
        self.rotation_point = rotation_point
        # Required for RectangleSelector with axes aspect ratio != 1
        # The patch is defined in data coordinates and when changing the
        # selector with square modifier and not in data coordinates, we need
        # to correct for the aspect ratio difference between the data and
        # display coordinate systems. Its value is typically provide by
        # Axes._get_aspect_ratio()
        self._aspect_ratio_correction = 1.0
        self._convert_units()  # Validate the inputs.

    def get_path(self):
        """Return the vertices of the rectangle."""
        return Path.unit_rectangle()

    def _convert_units(self):
        """Convert bounds of the rectangle."""
        x0 = self.convert_xunits(self._x0)
        y0 = self.convert_yunits(self._y0)
        x1 = self.convert_xunits(self._x0 + self._width)
        y1 = self.convert_yunits(self._y0 + self._height)
        return x0, y0, x1, y1

    def get_patch_transform(self):
        # Note: This cannot be called until after this has been added to
        # an Axes, otherwise unit conversion will fail. This makes it very
        # important to call the accessor method and not directly access the
        # transformation member variable.
        bbox = self.get_bbox()
        if self.rotation_point == 'center':
            width, height = bbox.x1 - bbox.x0, bbox.y1 - bbox.y0
            rotation_point = bbox.x0 + width / 2., bbox.y0 + height / 2.
        elif self.rotation_point == 'xy':
            rotation_point = bbox.x0, bbox.y0
        else:
            rotation_point = self.rotation_point
        return transforms.BboxTransformTo(bbox) \
                + transforms.Affine2D() \
                .translate(-rotation_point[0], -rotation_point[1]) \
                .scale(1, self._aspect_ratio_correction) \
                .rotate_deg(self.angle) \
                .scale(1, 1 / self._aspect_ratio_correction) \
                .translate(*rotation_point)

    @property
    def rotation_point(self):
        """The rotation point of the patch."""
        return self._rotation_point

    @rotation_point.setter
    def rotation_point(self, value):
        if value in ['center', 'xy'] or (
                isinstance(value, tuple) and len(value) == 2 and
                isinstance(value[0], Number) and isinstance(value[1], Number)
                ):
            self._rotation_point = value
        else:
            raise ValueError("`rotation_point` must be one of "
                             "{'xy', 'center', (number, number)}.")

    def get_x(self):
        """Return the left coordinate of the rectangle."""
        return self._x0

    def get_y(self):
        """Return the bottom coordinate of the rectangle."""
        return self._y0

    def get_xy(self):
        """Return the left and bottom coords of the rectangle as a tuple."""
        return self._x0, self._y0

    def get_corners(self):
        """
        Return the corners of the rectangle, moving anti-clockwise from
        (x0, y0).
        """
        return self.get_patch_transform().transform(
            [(0, 0), (1, 0), (1, 1), (0, 1)])

    def get_center(self):
        """Return the centre of the rectangle."""
        return self.get_patch_transform().transform((0.5, 0.5))

    def get_width(self):
        """Return the width of the rectangle."""
        return self._width

    def get_height(self):
        """Return the height of the rectangle."""
        return self._height

    def get_angle(self):
        """Get the rotation angle in degrees."""
        return self.angle

    def set_x(self, x):
        """Set the left coordinate of the rectangle."""
        self._x0 = x
        self.stale = True

    def set_y(self, y):
        """Set the bottom coordinate of the rectangle."""
        self._y0 = y
        self.stale = True

    def set_angle(self, angle):
        """
        Set the rotation angle in degrees.

        The rotation is performed anti-clockwise around *xy*.
        """
        self.angle = angle
        self.stale = True

    def set_xy(self, xy):
        """
        Set the left and bottom coordinates of the rectangle.

        Parameters
        ----------
        xy : (float, float)
        """
        self._x0, self._y0 = xy
        self.stale = True

    def set_width(self, w):
        """Set the width of the rectangle."""
        self._width = w
        self.stale = True

    def set_height(self, h):
        """Set the height of the rectangle."""
        self._height = h
        self.stale = True

    def set_bounds(self, *args):
        """
        Set the bounds of the rectangle as *left*, *bottom*, *width*, *height*.

        The values may be passed as separate parameters or as a tuple::

            set_bounds(left, bottom, width, height)
            set_bounds((left, bottom, width, height))

        .. ACCEPTS: (left, bottom, width, height)
        """
        if len(args) == 1:
            l, b, w, h = args[0]
        else:
            l, b, w, h = args
        self._x0 = l
        self._y0 = b
        self._width = w
        self._height = h
        self.stale = True

    def get_bbox(self):
        """Return the `.Bbox`."""
        x0, y0, x1, y1 = self._convert_units()
        return transforms.Bbox.from_extents(x0, y0, x1, y1)

    xy = property(get_xy, set_xy)
