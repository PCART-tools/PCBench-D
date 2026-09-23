    def __init__(self, control_points):
        _o = len(control_points)
        self._orders = np.arange(_o)

        _coeff = BezierSegment._binom_coeff[_o - 1]
        xx, yy = np.asarray(control_points).T
        self._px = xx * _coeff
        self._py = yy * _coeff
