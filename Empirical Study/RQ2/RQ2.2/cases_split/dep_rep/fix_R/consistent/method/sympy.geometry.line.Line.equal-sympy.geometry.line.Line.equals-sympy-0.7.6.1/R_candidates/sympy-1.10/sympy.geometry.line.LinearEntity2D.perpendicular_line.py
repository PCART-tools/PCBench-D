    def perpendicular_line(self, p):
        """Create a new Line perpendicular to this linear entity which passes
        through the point `p`.

        Parameters
        ==========

        p : Point

        Returns
        =======

        line : Line

        See Also
        ========

        sympy.geometry.line.LinearEntity.is_perpendicular, perpendicular_segment

        Examples
        ========

        >>> from sympy import Point, Line
        >>> p1, p2, p3 = Point(0, 0), Point(2, 3), Point(-2, 2)
        >>> l1 = Line(p1, p2)
        >>> l2 = l1.perpendicular_line(p3)
        >>> p3 in l2
        True
        >>> l1.is_perpendicular(l2)
        True

        """
        p = Point(p, dim=self.ambient_dimension)
        # any two lines in R^2 intersect, so blindly making
        # a line through p in an orthogonal direction will work
        return Line(p, p + self.direction.orthogonal_direction)
