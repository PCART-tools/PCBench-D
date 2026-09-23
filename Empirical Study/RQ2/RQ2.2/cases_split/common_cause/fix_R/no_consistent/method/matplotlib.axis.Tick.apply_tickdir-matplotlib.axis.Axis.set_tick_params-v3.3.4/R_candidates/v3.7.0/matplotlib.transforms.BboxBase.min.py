    @property
    def min(self):
        """The bottom-left corner of the bounding box."""
        return np.min(self.get_points(), axis=0)
