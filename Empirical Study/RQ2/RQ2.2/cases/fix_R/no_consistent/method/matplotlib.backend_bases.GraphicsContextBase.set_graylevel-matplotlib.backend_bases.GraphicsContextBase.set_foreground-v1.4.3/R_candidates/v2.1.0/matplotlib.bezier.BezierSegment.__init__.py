    def __init__(self, control_points):
        """
        *control_points* : location of contol points. It needs have a
         shpae of n * 2, where n is the order of the bezier line. 1<=
         n <= 3 is supported.
        """
        _o = len(control_points)
        self._orders = np.arange(_o)
        _coeff = BezierSegment._binom_coeff[_o - 1]

        _control_points = np.asarray(control_points)
        xx = _control_points[:, 0]
        yy = _control_points[:, 1]

        self._px = xx * _coeff
        self._py = yy * _coeff
