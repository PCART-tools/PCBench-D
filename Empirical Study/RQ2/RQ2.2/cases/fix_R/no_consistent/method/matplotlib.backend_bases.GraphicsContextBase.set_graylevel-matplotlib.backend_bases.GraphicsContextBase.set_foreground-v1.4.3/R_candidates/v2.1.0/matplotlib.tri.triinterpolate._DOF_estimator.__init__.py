    def __init__(self, interpolator, **kwargs):
        if not isinstance(interpolator, CubicTriInterpolator):
            raise ValueError("Expected a CubicTriInterpolator object")
        self._pts = interpolator._pts
        self._tris_pts = interpolator._tris_pts
        self.z = interpolator._z
        self._triangles = interpolator._triangles
        (self._unit_x, self._unit_y) = (interpolator._unit_x,
                                        interpolator._unit_y)
        self.dz = self.compute_dz(**kwargs)
        self.compute_dof_from_df()
