    @property
    def ymax(self):
        """The top edge of the bounding box."""
        return np.max(self.get_points()[:, 1])
