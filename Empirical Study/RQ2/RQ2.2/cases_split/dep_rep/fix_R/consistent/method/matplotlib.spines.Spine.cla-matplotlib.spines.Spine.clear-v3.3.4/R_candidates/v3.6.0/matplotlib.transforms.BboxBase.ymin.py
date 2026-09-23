    @property
    def ymin(self):
        """The bottom edge of the bounding box."""
        return np.min(self.get_points()[:, 1])
