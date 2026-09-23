    @property
    def max(self):
        """
        (property) :attr:`max` is the top-right corner of the bounding box.
        """
        return np.max(self.get_points(), axis=0)
