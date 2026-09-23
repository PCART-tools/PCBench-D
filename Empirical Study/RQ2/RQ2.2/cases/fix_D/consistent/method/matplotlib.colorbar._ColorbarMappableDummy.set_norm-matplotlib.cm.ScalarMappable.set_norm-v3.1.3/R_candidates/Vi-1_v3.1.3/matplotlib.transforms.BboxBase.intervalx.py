    @property
    def intervalx(self):
        """
        The pair of *x* coordinates that define the bounding box.

        This is not guaranteed to be sorted from left to right.
        """
        return self.get_points()[:, 0]
