    def __init__(self, triangulation, z, trifinder=None):
        TriInterpolator.__init__(self, triangulation, z, trifinder)

        # Store plane coefficients for fast interpolation calculations.
        self._plane_coefficients = \
            self._triangulation.calculate_plane_coefficients(self._z)
