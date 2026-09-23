    def director_circle(self):
        """
        Returns a Circle consisting of all points where two perpendicular
        tangent lines to the ellipse cross each other.

        Returns
        =======

        Circle
            A director circle returned as a geometric object.

        Examples
        ========

        >>> from sympy import Ellipse, Point, symbols
        >>> c = Point(3,8)
        >>> Ellipse(c, 7, 9).director_circle()
        Circle(Point2D(3, 8), sqrt(130))
        >>> a, b = symbols('a b')
        >>> Ellipse(c, a, b).director_circle()
        Circle(Point2D(3, 8), sqrt(a**2 + b**2))

        References
        ==========

        .. [1] https://en.wikipedia.org/wiki/Director_circle

        """
        return Circle(self.center, sqrt(self.hradius**2 + self.vradius**2))
