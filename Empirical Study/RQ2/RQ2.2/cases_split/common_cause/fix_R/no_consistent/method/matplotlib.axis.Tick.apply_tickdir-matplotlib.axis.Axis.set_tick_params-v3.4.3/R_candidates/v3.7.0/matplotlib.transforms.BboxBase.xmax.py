    @property
    def xmax(self):
        """The right edge of the bounding box."""
        return np.max(self.get_points()[:, 0])
