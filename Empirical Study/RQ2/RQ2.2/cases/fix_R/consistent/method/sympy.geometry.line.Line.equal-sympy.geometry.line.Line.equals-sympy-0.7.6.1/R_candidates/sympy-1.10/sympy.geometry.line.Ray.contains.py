    def contains(self, other):
        """
        Is other GeometryEntity contained in this Ray?

        Examples
        ========

        >>> from sympy import Ray,Point,Segment
        >>> p1, p2 = Point(0, 0), Point(4, 4)
        >>> r = Ray(p1, p2)
        >>> r.contains(p1)
        True
        >>> r.contains((1, 1))
        True
        >>> r.contains((1, 3))
        False
        >>> s = Segment((1, 1), (2, 2))
        >>> r.contains(s)
        True
        >>> s = Segment((1, 2), (2, 5))
        >>> r.contains(s)
        False
        >>> r1 = Ray((2, 2), (3, 3))
        >>> r.contains(r1)
        True
        >>> r1 = Ray((2, 2), (3, 5))
        >>> r.contains(r1)
        False
        """
        if not isinstance(other, GeometryEntity):
            other = Point(other, dim=self.ambient_dimension)
        if isinstance(other, Point):
            if Point.is_collinear(self.p1, self.p2, other):
                # if we're in the direction of the ray, our
                # direction vector dot the ray's direction vector
                # should be non-negative
                return bool((self.p2 - self.p1).dot(other - self.p1) >= S.Zero)
            return False
        elif isinstance(other, Ray):
            if Point.is_collinear(self.p1, self.p2, other.p1, other.p2):
                return bool((self.p2 - self.p1).dot(other.p2 - other.p1) > S.Zero)
            return False
        elif isinstance(other, Segment):
            return other.p1 in self and other.p2 in self

        # No other known entity can be contained in a Ray
        return False
