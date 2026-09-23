    def __init__(self, control_points):
        self._cpoints = np.asarray(control_points)
        self._N, self._d = self._cpoints.shape
        self._orders = np.arange(self._N)
        coeff = [math.factorial(self._N - 1)
                 // (math.factorial(i) * math.factorial(self._N - 1 - i))
                 for i in range(self._N)]
        self._px = (self._cpoints.T * coeff).T
