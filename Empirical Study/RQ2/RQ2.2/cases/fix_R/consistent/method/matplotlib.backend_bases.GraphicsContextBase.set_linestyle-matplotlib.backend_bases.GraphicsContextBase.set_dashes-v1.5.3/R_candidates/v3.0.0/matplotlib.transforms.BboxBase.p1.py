    @property
    def p1(self):
        """
        :attr:`p1` is the second pair of (*x*, *y*) coordinates that
        define the bounding box.  It is not guaranteed to be the top-right
        corner.  For that, use :attr:`max`.
        """
        return self.get_points()[1]
