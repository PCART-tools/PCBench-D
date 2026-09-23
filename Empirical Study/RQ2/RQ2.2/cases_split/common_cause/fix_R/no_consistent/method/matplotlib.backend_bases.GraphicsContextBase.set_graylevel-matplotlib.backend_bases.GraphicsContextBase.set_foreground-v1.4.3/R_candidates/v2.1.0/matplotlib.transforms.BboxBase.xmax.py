    @property
    def xmax(self):
        """
        (property) :attr:`xmax` is the right edge of the bounding box.
        """
        return np.max(self.get_points()[:, 0])
