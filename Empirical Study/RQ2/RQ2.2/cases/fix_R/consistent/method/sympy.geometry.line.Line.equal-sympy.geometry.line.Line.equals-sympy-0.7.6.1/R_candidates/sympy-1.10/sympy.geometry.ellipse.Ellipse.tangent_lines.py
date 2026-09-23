    def tangent_lines(self, p):
        """Tangent lines between `p` and the ellipse.

        If `p` is on the ellipse, returns the tangent line through point `p`.
        Otherwise, returns the tangent line(s) from `p` to the ellipse, or
        None if no tangent line is possible (e.g., `p` inside ellipse).

        Parameters
        ==========

        p : Point

        Returns
        =======

        tangent_lines : list with 1 or 2 Lines

        Raises
        ======

        NotImplementedError
            Can only find tangent lines for a point, `p`, on the ellipse.

        See Also
        ========

        sympy.geometry.point.Point, sympy.geometry.line.Line

        Examples
        ========

        >>> from sympy import Point, Ellipse
        >>> e1 = Ellipse(Point(0, 0), 3, 2)
        >>> e1.tangent_lines(Point(3, 0))
        [Line2D(Point2D(3, 0), Point2D(3, -12))]

        """
        p = Point(p, dim=2)
        if self.encloses_point(p):
            return []

        if p in self:
            delta = self.center - p
            rise = (self.vradius**2)*delta.x
            run = -(self.hradius**2)*delta.y
            p2 = Point(simplify(p.x + run),
                       simplify(p.y + rise))
            return [Line(p, p2)]
        else:
            if len(self.foci) == 2:
                f1, f2 = self.foci
                maj = self.hradius
                test = (2*maj -
                        Point.distance(f1, p) -
                        Point.distance(f2, p))
            else:
                test = self.radius - Point.distance(self.center, p)
            if test.is_number and test.is_positive:
                return []
            # else p is outside the ellipse or we can't tell. In case of the
            # latter, the solutions returned will only be valid if
            # the point is not inside the ellipse; if it is, nan will result.
            x, y = Dummy('x'), Dummy('y')
            eq = self.equation(x, y)
            dydx = idiff(eq, y, x)
            slope = Line(p, Point(x, y)).slope

            # TODO: Replace solve with solveset, when this line is tested
            tangent_points = solve([slope - dydx, eq], [x, y])

            # handle horizontal and vertical tangent lines
            if len(tangent_points) == 1:
                if tangent_points[0][
                           0] == p.x or tangent_points[0][1] == p.y:
                    return [Line(p, p + Point(1, 0)), Line(p, p + Point(0, 1))]
                else:
                    return [Line(p, p + Point(0, 1)), Line(p, tangent_points[0])]

            # others
            return [Line(p, tangent_points[0]), Line(p, tangent_points[1])]
