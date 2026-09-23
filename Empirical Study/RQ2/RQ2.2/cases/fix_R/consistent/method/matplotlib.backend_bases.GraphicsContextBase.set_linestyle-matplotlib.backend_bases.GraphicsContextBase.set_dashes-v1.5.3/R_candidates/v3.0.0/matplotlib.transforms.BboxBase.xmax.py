    @property
    def xmax(self):
        """
        :attr:`xmax` is the right edge of the bounding box.
        """
        return np.max(self.get_points()[:, 0])
