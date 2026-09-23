    def normal_lines(self, p, prec=None):
        """Normal lines between `p` and the ellipse.

        Parameters
        ==========

        p : Point

        Returns
        =======

        normal_lines : list with 1, 2 or 4 Lines

        Examples
        ========

        >>> from sympy import Point, Ellipse
        >>> e = Ellipse((0, 0), 2, 3)
        >>> c = e.center
        >>> e.normal_lines(c + Point(1, 0))
        [Line2D(Point2D(0, 0), Point2D(1, 0))]
        >>> e.normal_lines(c)
        [Line2D(Point2D(0, 0), Point2D(0, 1)), Line2D(Point2D(0, 0), Point2D(1, 0))]

        Off-axis points require the solution of a quartic equation. This
        often leads to very large expressions that may be of little practical
        use. An approximate solution of `prec` digits can be obtained by
        passing in the desired value:

        >>> e.normal_lines((3, 3), prec=2)
        [Line2D(Point2D(-0.81, -2.7), Point2D(0.19, -1.2)),
        Line2D(Point2D(1.5, -2.0), Point2D(2.5, -2.7))]

        Whereas the above solution has an operation count of 12, the exact
        solution has an operation count of 2020.
        """
        p = Point(p, dim=2)

        # XXX change True to something like self.angle == 0 if the arbitrarily
        # rotated ellipse is introduced.
        # https://github.com/sympy/sympy/issues/2815)
        if True:
            rv = []
            if p.x == self.center.x:
                rv.append(Line(self.center, slope=oo))
            if p.y == self.center.y:
                rv.append(Line(self.center, slope=0))
            if rv:
                # at these special orientations of p either 1 or 2 normals
                # exist and we are done
                return rv

        # find the 4 normal points and construct lines through them with
        # the corresponding slope
        x, y = Dummy('x', real=True), Dummy('y', real=True)
        eq = self.equation(x, y)
        dydx = idiff(eq, y, x)
        norm = -1/dydx
        slope = Line(p, (x, y)).slope
        seq = slope - norm

        # TODO: Replace solve with solveset, when this line is tested
        yis = solve(seq, y)[0]
        xeq = eq.subs(y, yis).as_numer_denom()[0].expand()
        if len(xeq.free_symbols) == 1:
            try:
                # this is so much faster, it's worth a try
                xsol = Poly(xeq, x).real_roots()
            except (DomainError, PolynomialError, NotImplementedError):
                # TODO: Replace solve with solveset, when these lines are tested
                xsol = _nsort(solve(xeq, x), separated=True)[0]
            points = [Point(i, solve(eq.subs(x, i), y)[0]) for i in xsol]
        else:
            raise NotImplementedError(
                'intersections for the general ellipse are not supported')
        slopes = [norm.subs(zip((x, y), pt.args)) for pt in points]
        if prec is not None:
            points = [pt.n(prec) for pt in points]
            slopes = [i if _not_a_coeff(i) else i.n(prec) for i in slopes]
        return [Line(pt, slope=s) for pt, s in zip(points, slopes)]
