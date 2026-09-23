    def section_modulus(self, point=None):
        """Returns a tuple with the section modulus of an ellipse

        Section modulus is a geometric property of an ellipse defined as the
        ratio of second moment of area to the distance of the extreme end of
        the ellipse from the centroidal axis.

        Parameters
        ==========

        point : Point, two-tuple of sympifyable objects, or None(default=None)
            point is the point at which section modulus is to be found.
            If "point=None" section modulus will be calculated for the
            point farthest from the centroidal axis of the ellipse.

        Returns
        =======

        S_x, S_y: numbers or SymPy expressions
                  S_x is the section modulus with respect to the x-axis
                  S_y is the section modulus with respect to the y-axis
                  A negative sign indicates that the section modulus is
                  determined for a point below the centroidal axis.

        Examples
        ========

        >>> from sympy import Symbol, Ellipse, Circle, Point2D
        >>> d = Symbol('d', positive=True)
        >>> c = Circle((0, 0), d/2)
        >>> c.section_modulus()
        (pi*d**3/32, pi*d**3/32)
        >>> e = Ellipse(Point2D(0, 0), 2, 4)
        >>> e.section_modulus()
        (8*pi, 4*pi)
        >>> e.section_modulus((2, 2))
        (16*pi, 4*pi)

        References
        ==========

        .. [1] https://en.wikipedia.org/wiki/Section_modulus

        """
        x_c, y_c = self.center
        if point is None:
            # taking x and y as maximum distances from centroid
            x_min, y_min, x_max, y_max = self.bounds
            y = max(y_c - y_min, y_max - y_c)
            x = max(x_c - x_min, x_max - x_c)
        else:
            # taking x and y as distances of the given point from the center
            point = Point2D(point)
            y = point.y - y_c
            x = point.x - x_c

        second_moment = self.second_moment_of_area()
        S_x = second_moment[0]/y
        S_y = second_moment[1]/x

        return S_x, S_y
