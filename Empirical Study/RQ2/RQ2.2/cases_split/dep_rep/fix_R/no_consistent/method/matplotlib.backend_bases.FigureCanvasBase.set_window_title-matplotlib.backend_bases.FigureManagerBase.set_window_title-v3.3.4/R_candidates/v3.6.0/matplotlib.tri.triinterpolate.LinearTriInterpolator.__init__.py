    def __init__(self, triangulation, z, trifinder=None):
        super().__init__(triangulation, z, trifinder)

        # Store plane coefficients for fast interpolation calculations.
        self._plane_coefficients = \
            self._triangulation.calculate_plane_coefficients(self._z)
