    @property
    def ymin(self):
        """
        (property) :attr:`ymin` is the bottom edge of the bounding box.
        """
        return np.min(self.get_points()[:, 1])
