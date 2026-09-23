    @property
    def xmin(self):
        """
        (property) :attr:`xmin` is the left edge of the bounding box.
        """
        return np.min(self.get_points()[:, 0])
