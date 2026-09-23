    def parameter_value(self, other, t):
        """Return the parameter corresponding to the given point.
        Evaluating an arbitrary point of the entity at this parameter
        value will return the given point.

        Examples
        ========

        >>> from sympy import Line, Point
        >>> from sympy.abc import t
        >>> a = Point(0, 0)
        >>> b = Point(2, 2)
        >>> Line(a, b).parameter_value((1, 1), t)
        {t: 1/2}
        >>> Line(a, b).arbitrary_point(t).subs(_)
        Point2D(1, 1)
        """
        from sympy.geometry.point import Point
        from sympy.solvers.solvers import solve
        if not isinstance(other, GeometryEntity):
            other = Point(other, dim=self.ambient_dimension)
        if not isinstance(other, Point):
            raise ValueError("other must be a point")
        T = Dummy('t', real=True)
        sol = solve(self.arbitrary_point(T) - other, T, dict=True)
        if not sol:
            raise ValueError("Given point is not on %s" % func_name(self))
        return {t: sol[0][T]}
