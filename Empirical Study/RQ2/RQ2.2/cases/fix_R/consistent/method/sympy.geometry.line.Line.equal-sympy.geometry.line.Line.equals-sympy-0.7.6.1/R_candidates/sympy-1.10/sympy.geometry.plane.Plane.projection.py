    def projection(self, pt):
        """Project the given point onto the plane along the plane normal.

        Parameters
        ==========

        Point or Point3D

        Returns
        =======

        Point3D

        Examples
        ========

        >>> from sympy import Plane, Point3D
        >>> A = Plane(Point3D(1, 1, 2), normal_vector=(1, 1, 1))

        The projection is along the normal vector direction, not the z
        axis, so (1, 1) does not project to (1, 1, 2) on the plane A:

        >>> b = Point3D(1, 1)
        >>> A.projection(b)
        Point3D(5/3, 5/3, 2/3)
        >>> _ in A
        True

        But the point (1, 1, 2) projects to (1, 1) on the XY-plane:

        >>> XY = Plane((0, 0, 0), (0, 0, 1))
        >>> XY.projection((1, 1, 2))
        Point3D(1, 1, 0)
        """
        rv = Point(pt, dim=3)
        if rv in self:
            return rv
        return self.intersection(Line3D(rv, rv + Point3D(self.normal_vector)))[0]
