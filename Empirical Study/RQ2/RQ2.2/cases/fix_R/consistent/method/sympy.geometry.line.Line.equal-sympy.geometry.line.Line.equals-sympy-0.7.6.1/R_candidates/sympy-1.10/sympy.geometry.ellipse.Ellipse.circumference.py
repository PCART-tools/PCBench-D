    @property
    def circumference(self):
        """The circumference of the ellipse.

        Examples
        ========

        >>> from sympy import Point, Ellipse
        >>> p1 = Point(0, 0)
        >>> e1 = Ellipse(p1, 3, 1)
        >>> e1.circumference
        12*elliptic_e(8/9)

        """
        if self.eccentricity == 1:
            # degenerate
            return 4*self.major
        elif self.eccentricity == 0:
            # circle
            return 2*pi*self.hradius
        else:
            return 4*self.major*elliptic_e(self.eccentricity**2)
