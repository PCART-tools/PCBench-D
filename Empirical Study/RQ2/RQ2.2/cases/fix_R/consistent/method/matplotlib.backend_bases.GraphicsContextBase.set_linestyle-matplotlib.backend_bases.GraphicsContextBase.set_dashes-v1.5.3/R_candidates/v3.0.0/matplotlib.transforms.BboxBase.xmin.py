    @property
    def xmin(self):
        """
        :attr:`xmin` is the left edge of the bounding box.
        """
        return np.min(self.get_points()[:, 0])
