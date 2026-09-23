    @property
    def p1(self):
        """The only defining point of the plane. Others can be obtained from the
        arbitrary_point method.

        See Also
        ========

        sympy.geometry.point.Point3D

        Examples
        ========

        >>> from sympy import Point3D, Plane
        >>> a = Plane(Point3D(1, 1, 1), Point3D(2, 3, 4), Point3D(2, 2, 2))
        >>> a.p1
        Point3D(1, 1, 1)

        """
        return self.args[0]
