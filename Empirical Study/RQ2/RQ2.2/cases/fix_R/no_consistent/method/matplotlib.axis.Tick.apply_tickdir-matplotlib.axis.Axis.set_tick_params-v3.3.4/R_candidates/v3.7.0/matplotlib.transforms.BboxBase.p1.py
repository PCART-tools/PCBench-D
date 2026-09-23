    @property
    def p1(self):
        """
        The second pair of (*x*, *y*) coordinates that define the bounding box.

        This is not guaranteed to be the top-right corner (for that, use
        :attr:`max`).
        """
        return self.get_points()[1]
