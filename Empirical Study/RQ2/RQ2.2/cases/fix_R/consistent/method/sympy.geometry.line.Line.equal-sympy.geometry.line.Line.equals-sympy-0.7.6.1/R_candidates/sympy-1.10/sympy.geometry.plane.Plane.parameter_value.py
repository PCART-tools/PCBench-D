    def parameter_value(self, other, u, v=None):
        """Return the parameter(s) corresponding to the given point.

        Examples
        ========

        >>> from sympy import pi, Plane
        >>> from sympy.abc import t, u, v
        >>> p = Plane((2, 0, 0), (0, 0, 1), (0, 1, 0))

        By default, the parameter value returned defines a point
        that is a distance of 1 from the Plane's p1 value and
        in line with the given point:

        >>> on_circle = p.arbitrary_point(t).subs(t, pi/4)
        >>> on_circle.distance(p.p1)
        1
        >>> p.parameter_value(on_circle, t)
        {t: pi/4}

        Moving the point twice as far from p1 does not change
        the parameter value:

        >>> off_circle = p.p1 + (on_circle - p.p1)*2
        >>> off_circle.distance(p.p1)
        2
        >>> p.parameter_value(off_circle, t)
        {t: pi/4}

        If the 2-value parameter is desired, supply the two
        parameter symbols and a replacement dictionary will
        be returned:

        >>> p.parameter_value(on_circle, u, v)
        {u: sqrt(10)/10, v: sqrt(10)/30}
        >>> p.parameter_value(off_circle, u, v)
        {u: sqrt(10)/5, v: sqrt(10)/15}
        """
        from sympy.geometry.point import Point
        if not isinstance(other, GeometryEntity):
            other = Point(other, dim=self.ambient_dimension)
        if not isinstance(other, Point):
            raise ValueError("other must be a point")
        if other == self.p1:
            return other
        if isinstance(u, Symbol) and v is None:
            delta = self.arbitrary_point(u) - self.p1
            eq = delta - (other - self.p1).unit
            sol = solve(eq, u, dict=True)
        elif isinstance(u, Symbol) and isinstance(v, Symbol):
            pt = self.arbitrary_point(u, v)
            sol = solve(pt - other, (u, v), dict=True)
        else:
            raise ValueError('expecting 1 or 2 symbols')
        if not sol:
            raise ValueError("Given point is not on %s" % func_name(self))
        return sol[0]  # {t: tval} or {u: uval, v: vval}
