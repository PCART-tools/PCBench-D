    @property
    def coordinates(self):
        """
        Returns the three coordinates of the Point.

        Examples
        ========

        >>> from sympy import Point3D
        >>> p = Point3D(0, 1, 2)
        >>> p.coordinates
        (0, 1, 2)
        """
        return self.args
