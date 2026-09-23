    @_docstring.dedent_interpd
    @_api.make_keyword_only("3.6", name="angle")
    def __init__(self, xy, width, height, angle=0.0,
                 theta1=0.0, theta2=360.0, **kwargs):
        """
        Parameters
        ----------
        xy : (float, float)
            The center of the ellipse.

        width : float
            The length of the horizontal axis.

        height : float
            The length of the vertical axis.

        angle : float
            Rotation of the ellipse in degrees (counterclockwise).

        theta1, theta2 : float, default: 0, 360
            Starting and ending angles of the arc in degrees. These values
            are relative to *angle*, e.g. if *angle* = 45 and *theta1* = 90
            the absolute starting angle is 135.
            Default *theta1* = 0, *theta2* = 360, i.e. a complete ellipse.
            The arc is drawn in the counterclockwise direction.
            Angles greater than or equal to 360, or smaller than 0, are
            represented by an equivalent angle in the range [0, 360), by
            taking the input value mod 360.

        Other Parameters
        ----------------
        **kwargs : `.Patch` properties
            Most `.Patch` properties are supported as keyword arguments,
            with the exception of *fill* and *facecolor* because filling is
            not supported.

        %(Patch:kwdoc)s
        """
        fill = kwargs.setdefault('fill', False)
        if fill:
            raise ValueError("Arc objects can not be filled")

        super().__init__(xy, width, height, angle=angle, **kwargs)

        self.theta1 = theta1
        self.theta2 = theta2
        (self._theta1, self._theta2, self._stretched_width,
         self._stretched_height) = self._theta_stretch()
        self._path = Path.arc(self._theta1, self._theta2)
