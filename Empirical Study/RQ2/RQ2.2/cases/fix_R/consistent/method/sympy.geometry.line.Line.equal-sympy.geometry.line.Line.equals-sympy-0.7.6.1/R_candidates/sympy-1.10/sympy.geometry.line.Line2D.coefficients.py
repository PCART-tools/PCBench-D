    @property
    def coefficients(self):
        """The coefficients (`a`, `b`, `c`) for `ax + by + c = 0`.

        See Also
        ========

        sympy.geometry.line.Line2D.equation

        Examples
        ========

        >>> from sympy import Point, Line
        >>> from sympy.abc import x, y
        >>> p1, p2 = Point(0, 0), Point(5, 3)
        >>> l = Line(p1, p2)
        >>> l.coefficients
        (-3, 5, 0)

        >>> p3 = Point(x, y)
        >>> l2 = Line(p1, p3)
        >>> l2.coefficients
        (-y, x, 0)

        """
        p1, p2 = self.points
        if p1.x == p2.x:
            return (S.One, S.Zero, -p1.x)
        elif p1.y == p2.y:
            return (S.Zero, S.One, -p1.y)
        return tuple([simplify(i) for i in
                      (self.p1.y - self.p2.y,
                       self.p2.x - self.p1.x,
                       self.p1.x*self.p2.y - self.p1.y*self.p2.x)])
