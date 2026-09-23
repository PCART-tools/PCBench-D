    @property
    def p0(self):
        """
        The first pair of (*x*, *y*) coordinates that define the bounding box.

        This is not guaranteed to be the bottom-left corner (for that, use
        :attr:`min`).
        """
        return self.get_points()[0]
