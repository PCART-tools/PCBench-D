    @property
    def xmin(self):
        """The left edge of the bounding box."""
        return np.min(self.get_points()[:, 0])
