    @property
    def ymax(self):
        """
        (property) :attr:`ymax` is the top edge of the bounding box.
        """
        return np.max(self.get_points()[:, 1])
