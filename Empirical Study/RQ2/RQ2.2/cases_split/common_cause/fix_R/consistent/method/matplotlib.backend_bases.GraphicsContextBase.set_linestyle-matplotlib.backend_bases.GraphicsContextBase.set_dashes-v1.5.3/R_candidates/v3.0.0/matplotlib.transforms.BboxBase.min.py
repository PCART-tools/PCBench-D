    @property
    def min(self):
        """
        :attr:`min` is the bottom-left corner of the bounding box.
        """
        return np.min(self.get_points(), axis=0)
