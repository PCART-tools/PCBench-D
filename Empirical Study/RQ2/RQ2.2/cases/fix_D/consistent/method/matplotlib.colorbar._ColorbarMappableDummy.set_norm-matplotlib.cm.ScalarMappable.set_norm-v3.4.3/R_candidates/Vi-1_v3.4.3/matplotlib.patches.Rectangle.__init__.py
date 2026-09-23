    @docstring.dedent_interpd
    def __init__(self, xy, width, height, angle=0.0, **kwargs):
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
            Rotation in degrees anti-clockwise about *xy*.

        Other Parameters
        ----------------
        **kwargs : `.Patch` properties
            %(Patch_kwdoc)s
        """
        super().__init__(**kwargs)
        self._x0 = xy[0]
        self._y0 = xy[1]
        self._width = width
        self._height = height
        self.angle = float(angle)
        self._convert_units()  # Validate the inputs.
