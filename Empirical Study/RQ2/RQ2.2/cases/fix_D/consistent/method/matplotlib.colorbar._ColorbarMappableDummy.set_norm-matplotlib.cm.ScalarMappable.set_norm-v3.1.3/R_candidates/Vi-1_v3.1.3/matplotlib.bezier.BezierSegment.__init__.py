    def __init__(self, control_points):
        """
        *control_points* : location of contol points. It needs have a
         shape of n * 2, where n is the order of the bezier line. 1<=
         n <= 3 is supported.
        """
        _o = len(control_points)
        self._orders = np.arange(_o)

        _coeff = BezierSegment._binom_coeff[_o - 1]
        xx, yy = np.asarray(control_points).T
        self._px = xx * _coeff
        self._py = yy * _coeff
