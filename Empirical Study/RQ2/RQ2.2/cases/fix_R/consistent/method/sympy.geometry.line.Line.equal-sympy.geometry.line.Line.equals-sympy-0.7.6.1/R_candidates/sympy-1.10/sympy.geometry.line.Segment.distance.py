    def distance(self, other):
        """
        Finds the shortest distance between a line segment and a point.

        Raises
        ======

        NotImplementedError is raised if `other` is not a Point

        Examples
        ========

        >>> from sympy import Point, Segment
        >>> p1, p2 = Point(0, 1), Point(3, 4)
        >>> s = Segment(p1, p2)
        >>> s.distance(Point(10, 15))
        sqrt(170)
        >>> s.distance((0, 12))
        sqrt(73)
        >>> from sympy import Point3D, Segment3D
        >>> p1, p2 = Point3D(0, 0, 3), Point3D(1, 1, 4)
        >>> s = Segment3D(p1, p2)
        >>> s.distance(Point3D(10, 15, 12))
        sqrt(341)
        >>> s.distance((10, 15, 12))
        sqrt(341)
        """
        if not isinstance(other, GeometryEntity):
            other = Point(other, dim=self.ambient_dimension)
        if isinstance(other, Point):
            vp1 = other - self.p1
            vp2 = other - self.p2

            dot_prod_sign_1 = self.direction.dot(vp1) >= 0
            dot_prod_sign_2 = self.direction.dot(vp2) <= 0
            if dot_prod_sign_1 and dot_prod_sign_2:
                return Line(self.p1, self.p2).distance(other)
            if dot_prod_sign_1 and not dot_prod_sign_2:
                return abs(vp2)
            if not dot_prod_sign_1 and dot_prod_sign_2:
                return abs(vp1)
        raise NotImplementedError()
