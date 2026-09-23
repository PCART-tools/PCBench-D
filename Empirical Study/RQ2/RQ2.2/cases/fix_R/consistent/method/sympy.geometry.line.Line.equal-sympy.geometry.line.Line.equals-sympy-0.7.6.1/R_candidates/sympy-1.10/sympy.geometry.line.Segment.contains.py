    def contains(self, other):
        """
        Is the other GeometryEntity contained within this Segment?

        Examples
        ========

        >>> from sympy import Point, Segment
        >>> p1, p2 = Point(0, 1), Point(3, 4)
        >>> s = Segment(p1, p2)
        >>> s2 = Segment(p2, p1)
        >>> s.contains(s2)
        True
        >>> from sympy import Point3D, Segment3D
        >>> p1, p2 = Point3D(0, 1, 1), Point3D(3, 4, 5)
        >>> s = Segment3D(p1, p2)
        >>> s2 = Segment3D(p2, p1)
        >>> s.contains(s2)
        True
        >>> s.contains((p1 + p2)/2)
        True
        """
        if not isinstance(other, GeometryEntity):
            other = Point(other, dim=self.ambient_dimension)
        if isinstance(other, Point):
            if Point.is_collinear(other, self.p1, self.p2):
                if isinstance(self, Segment2D):
                    # if it is collinear and is in the bounding box of the
                    # segment then it must be on the segment
                    vert = (1/self.slope).equals(0)
                    if vert is False:
                        isin = (self.p1.x - other.x)*(self.p2.x - other.x) <= 0
                        if isin in (True, False):
                            return isin
                    if vert is True:
                        isin = (self.p1.y - other.y)*(self.p2.y - other.y) <= 0
                        if isin in (True, False):
                            return isin
                # use the triangle inequality
                d1, d2 = other - self.p1, other - self.p2
                d = self.p2 - self.p1
                # without the call to simplify, SymPy cannot tell that an expression
                # like (a+b)*(a/2+b/2) is always non-negative.  If it cannot be
                # determined, raise an Undecidable error
                try:
                    # the triangle inequality says that |d1|+|d2| >= |d| and is strict
                    # only if other lies in the line segment
                    return bool(simplify(Eq(abs(d1) + abs(d2) - abs(d), 0)))
                except TypeError:
                    raise Undecidable("Cannot determine if {} is in {}".format(other, self))
        if isinstance(other, Segment):
            return other.p1 in self and other.p2 in self

        return False
