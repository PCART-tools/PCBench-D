    @property
    def zdirection(self):
        """The z direction of the ray.

        Positive infinity if the ray points in the positive z direction,
        negative infinity if the ray points in the negative z direction,
        or 0 if the ray is horizontal.

        See Also
        ========

        xdirection

        Examples
        ========

        >>> from sympy import Point3D, Ray3D
        >>> p1, p2, p3 = Point3D(0, 0, 0), Point3D(-1, -1, -1), Point3D(-1, 0, 0)
        >>> r1, r2 = Ray3D(p1, p2), Ray3D(p1, p3)
        >>> r1.ydirection
        -oo
        >>> r2.ydirection
        0
        >>> r2.zdirection
        0

        """
        if self.p1.z < self.p2.z:
            return S.Infinity
        elif self.p1.z == self.p2.z:
            return S.Zero
        else:
            return S.NegativeInfinity
