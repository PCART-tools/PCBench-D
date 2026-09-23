    @property
    def direction_ratio(self):
        """The direction ratio of a given line in 3D.

        See Also
        ========

        sympy.geometry.line.Line3D.equation

        Examples
        ========

        >>> from sympy import Point3D, Line3D
        >>> p1, p2 = Point3D(0, 0, 0), Point3D(5, 3, 1)
        >>> l = Line3D(p1, p2)
        >>> l.direction_ratio
        [5, 3, 1]
        """
        p1, p2 = self.points
        return p1.direction_ratio(p2)
