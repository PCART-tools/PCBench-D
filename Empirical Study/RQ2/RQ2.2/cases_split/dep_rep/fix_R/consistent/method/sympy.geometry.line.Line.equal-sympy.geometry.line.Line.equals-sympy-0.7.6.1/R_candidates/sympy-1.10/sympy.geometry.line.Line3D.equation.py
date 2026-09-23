    def equation(self, x='x', y='y', z='z', k=None):
        """Return the equations that define the line in 3D.

        Parameters
        ==========

        x : str, optional
            The name to use for the x-axis, default value is 'x'.
        y : str, optional
            The name to use for the y-axis, default value is 'y'.
        z : str, optional
            The name to use for the z-axis, default value is 'z'.
        k : str, optional
            .. deprecated:: 1.2
               The ``k`` flag is deprecated. It does nothing.

        Returns
        =======

        equation : Tuple of simultaneous equations

        Examples
        ========

        >>> from sympy import Point3D, Line3D, solve
        >>> from sympy.abc import x, y, z
        >>> p1, p2 = Point3D(1, 0, 0), Point3D(5, 3, 0)
        >>> l1 = Line3D(p1, p2)
        >>> eq = l1.equation(x, y, z); eq
        (-3*x + 4*y + 3, z)
        >>> solve(eq.subs(z, 0), (x, y, z))
        {x: 4*y/3 + 1}

        """
        if k is not None:
            sympy_deprecation_warning(
                """
                The 'k' argument to Line3D.equation() is deprecated. Is
                currently has no effect, so it may be omitted.
                """,
                deprecated_since_version="1.2",
                active_deprecations_target='deprecated-line3d-equation-k',
            )
        from sympy.solvers.solvers import solve
        x, y, z, k = [_symbol(i, real=True) for i in (x, y, z, 'k')]
        p1, p2 = self.points
        d1, d2, d3 = p1.direction_ratio(p2)
        x1, y1, z1 = p1
        eqs = [-d1*k + x - x1, -d2*k + y - y1, -d3*k + z - z1]
        # eliminate k from equations by solving first eq with k for k
        for i, e in enumerate(eqs):
            if e.has(k):
                kk = solve(eqs[i], k)[0]
                eqs.pop(i)
                break
        return Tuple(*[i.subs(k, kk).as_numer_denom()[0] for i in eqs])
