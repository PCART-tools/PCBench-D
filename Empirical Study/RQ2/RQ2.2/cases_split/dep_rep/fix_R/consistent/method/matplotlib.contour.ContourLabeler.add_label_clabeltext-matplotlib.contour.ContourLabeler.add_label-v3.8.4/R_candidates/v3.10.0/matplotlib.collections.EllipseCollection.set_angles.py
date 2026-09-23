    def set_angles(self, angles):
        """Set the angles of the first axes, degrees CCW from the x-axis."""
        self._angles = np.deg2rad(angles).ravel()
        self.stale = True
