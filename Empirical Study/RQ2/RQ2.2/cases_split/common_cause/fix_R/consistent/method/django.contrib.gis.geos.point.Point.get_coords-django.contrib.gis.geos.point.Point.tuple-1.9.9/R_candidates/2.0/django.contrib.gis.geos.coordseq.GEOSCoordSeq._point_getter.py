    @property
    def _point_getter(self):
        return self._get_point_3d if self.dims == 3 and self._z else self._get_point_2d
