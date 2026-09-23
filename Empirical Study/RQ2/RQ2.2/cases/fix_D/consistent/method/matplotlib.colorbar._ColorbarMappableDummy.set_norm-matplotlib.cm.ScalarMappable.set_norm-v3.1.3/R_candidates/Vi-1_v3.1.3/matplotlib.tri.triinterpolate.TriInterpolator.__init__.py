    def __init__(self, triangulation, z, trifinder=None):
        if not isinstance(triangulation, Triangulation):
            raise ValueError("Expected a Triangulation object")
        self._triangulation = triangulation

        self._z = np.asarray(z)
        if self._z.shape != self._triangulation.x.shape:
            raise ValueError("z array must have same length as triangulation x"
                             " and y arrays")

        if trifinder is not None and not isinstance(trifinder, TriFinder):
            raise ValueError("Expected a TriFinder object")
        self._trifinder = trifinder or self._triangulation.get_trifinder()

        # Default scaling factors : 1.0 (= no scaling)
        # Scaling may be used for interpolations for which the order of
        # magnitude of x, y has an impact on the interpolant definition.
        # Please refer to :meth:`_interpolate_multikeys` for details.
        self._unit_x = 1.0
        self._unit_y = 1.0

        # Default triangle renumbering: None (= no renumbering)
        # Renumbering may be used to avoid unnecessary computations
        # if complex calculations are done inside the Interpolator.
        # Please refer to :meth:`_interpolate_multikeys` for details.
        self._tri_renum = None
