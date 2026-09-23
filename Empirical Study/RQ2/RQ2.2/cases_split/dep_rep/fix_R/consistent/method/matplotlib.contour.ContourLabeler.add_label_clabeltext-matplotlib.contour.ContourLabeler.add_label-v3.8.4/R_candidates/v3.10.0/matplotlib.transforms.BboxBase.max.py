    @property
    def max(self):
        """The top-right corner of the bounding box."""
        return np.max(self.get_points(), axis=0)
