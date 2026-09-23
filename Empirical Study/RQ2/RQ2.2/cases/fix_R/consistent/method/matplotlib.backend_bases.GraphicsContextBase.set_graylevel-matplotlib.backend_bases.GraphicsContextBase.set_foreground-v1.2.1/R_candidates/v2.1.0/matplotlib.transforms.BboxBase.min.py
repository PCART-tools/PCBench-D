    @property
    def min(self):
        """
        (property) :attr:`min` is the bottom-left corner of the bounding box.
        """
        return np.min(self.get_points(), axis=0)
