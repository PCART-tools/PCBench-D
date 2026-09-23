    @rotation.setter
    def rotation(self, value):
        # Restrict to a limited range of rotation [-45°, 45°] to avoid changing
        # order of handles
        if -45 <= value and value <= 45:
            self._rotation = np.deg2rad(value)
            # call extents setter to draw shape and update handles positions
            self.extents = self.extents
