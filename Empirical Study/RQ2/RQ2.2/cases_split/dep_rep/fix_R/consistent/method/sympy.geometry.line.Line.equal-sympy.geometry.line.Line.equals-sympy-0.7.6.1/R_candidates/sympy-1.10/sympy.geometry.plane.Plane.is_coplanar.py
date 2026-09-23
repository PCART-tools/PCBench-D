    def is_coplanar(self, o):
        """ Returns True if `o` is coplanar with self, else False.

        Examples
        ========

        >>> from sympy import Plane
        >>> o = (0, 0, 0)
        >>> p = Plane(o, (1, 1, 1))
        >>> p2 = Plane(o, (2, 2, 2))
        >>> p == p2
        False
        >>> p.is_coplanar(p2)
        True
        """
        if isinstance(o, Plane):
            x, y, z = map(Dummy, 'xyz')
            return not cancel(self.equation(x, y, z)/o.equation(x, y, z)).has(x, y, z)
        if isinstance(o, Point3D):
            return o in self
        elif isinstance(o, LinearEntity3D):
            return all(i in self for i in self)
        elif isinstance(o, GeometryEntity):  # XXX should only be handling 2D objects now
            return all(i == 0 for i in self.normal_vector[:2])
