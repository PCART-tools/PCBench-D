    @property
    def direction(self):
        """The direction vector of the LinearEntity.

        Returns
        =======

        p : a Point; the ray from the origin to this point is the
            direction of `self`

        Examples
        ========

        >>> from sympy import Line
        >>> a, b = (1, 1), (1, 3)
        >>> Line(a, b).direction
        Point2D(0, 2)
        >>> Line(b, a).direction
        Point2D(0, -2)

        This can be reported so the distance from the origin is 1:

        >>> Line(b, a).direction.unit
        Point2D(0, -1)

        See Also
        ========

        sympy.geometry.point.Point.unit

        """
        return self.p2 - self.p1
