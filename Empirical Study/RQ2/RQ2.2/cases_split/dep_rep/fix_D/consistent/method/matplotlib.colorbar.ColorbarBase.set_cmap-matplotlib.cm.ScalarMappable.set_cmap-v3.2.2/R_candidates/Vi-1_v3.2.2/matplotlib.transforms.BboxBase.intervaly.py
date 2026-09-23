    @property
    def intervaly(self):
        """
        The pair of *y* coordinates that define the bounding box.

        This is not guaranteed to be sorted from bottom to top.
        """
        return self.get_points()[:, 1]
