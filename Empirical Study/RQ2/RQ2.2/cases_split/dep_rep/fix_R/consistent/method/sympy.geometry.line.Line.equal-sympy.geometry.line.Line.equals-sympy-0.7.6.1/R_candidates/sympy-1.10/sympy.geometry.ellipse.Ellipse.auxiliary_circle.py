    def auxiliary_circle(self):
        """Returns a Circle whose diameter is the major axis of the ellipse.

        Examples
        ========

        >>> from sympy import Ellipse, Point, symbols
        >>> c = Point(1, 2)
        >>> Ellipse(c, 8, 7).auxiliary_circle()
        Circle(Point2D(1, 2), 8)
        >>> a, b = symbols('a b')
        >>> Ellipse(c, a, b).auxiliary_circle()
        Circle(Point2D(1, 2), Max(a, b))
        """
        return Circle(self.center, Max(self.hradius, self.vradius))
