    def contains(self, other):
        """
        Return True if `other` is on this Line, or False otherwise.

        Examples
        ========

        >>> from sympy import Line,Point
        >>> p1, p2 = Point(0, 1), Point(3, 4)
        >>> l = Line(p1, p2)
        >>> l.contains(p1)
        True
        >>> l.contains((0, 1))
        True
        >>> l.contains((0, 0))
        False
        >>> a = (0, 0, 0)
        >>> b = (1, 1, 1)
        >>> c = (2, 2, 2)
        >>> l1 = Line(a, b)
        >>> l2 = Line(b, a)
        >>> l1 == l2
        False
        >>> l1 in l2
        True

        """
        if not isinstance(other, GeometryEntity):
            other = Point(other, dim=self.ambient_dimension)
        if isinstance(other, Point):
            return Point.is_collinear(other, self.p1, self.p2)
        if isinstance(other, LinearEntity):
            return Point.is_collinear(self.p1, self.p2, other.p1, other.p2)
        return False
