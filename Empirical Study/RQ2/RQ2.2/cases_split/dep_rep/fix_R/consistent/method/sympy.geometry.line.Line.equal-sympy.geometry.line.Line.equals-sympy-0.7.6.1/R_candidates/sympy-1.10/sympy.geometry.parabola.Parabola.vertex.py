    @property
    def vertex(self):
        """The vertex of the parabola.

        Returns
        =======

        vertex : Point

        See Also
        ========

        sympy.geometry.point.Point

        Examples
        ========

        >>> from sympy import Parabola, Point, Line
        >>> p1 = Parabola(Point(0, 0), Line(Point(5, 8), Point(7, 8)))
        >>> p1.vertex
        Point2D(0, 4)

        """
        focus = self.focus
        if (self.axis_of_symmetry.slope == 0):
            vertex = Point(focus.args[0] - self.p_parameter, focus.args[1])
        else:
            vertex = Point(focus.args[0], focus.args[1] - self.p_parameter)

        return vertex
