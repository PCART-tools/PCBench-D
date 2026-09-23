    @property
    def max(self):
        """
        :attr:`max` is the top-right corner of the bounding box.
        """
        return np.max(self.get_points(), axis=0)
