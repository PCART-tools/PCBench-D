    def __init__(self, Interpolator):
        self._eccs = Interpolator._eccs
        _DOF_estimator_geom.__init__(self, Interpolator)
