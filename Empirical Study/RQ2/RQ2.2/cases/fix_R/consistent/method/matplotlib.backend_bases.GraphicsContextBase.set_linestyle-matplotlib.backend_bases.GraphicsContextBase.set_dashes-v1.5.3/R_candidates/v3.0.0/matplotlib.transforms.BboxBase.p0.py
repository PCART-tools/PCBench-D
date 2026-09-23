    @property
    def p0(self):
        """
        :attr:`p0` is the first pair of (*x*, *y*) coordinates that
        define the bounding box.  It is not guaranteed to be the bottom-left
        corner.  For that, use :attr:`min`.
        """
        return self.get_points()[0]
