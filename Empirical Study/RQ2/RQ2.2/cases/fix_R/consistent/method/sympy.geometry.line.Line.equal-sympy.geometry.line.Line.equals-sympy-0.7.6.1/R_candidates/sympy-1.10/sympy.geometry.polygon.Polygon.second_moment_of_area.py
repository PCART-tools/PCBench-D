    def second_moment_of_area(self, point=None):
        """Returns the second moment and product moment of area of a two dimensional polygon.

        Parameters
        ==========

        point : Point, two-tuple of sympifyable objects, or None(default=None)
            point is the point about which second moment of area is to be found.
            If "point=None" it will be calculated about the axis passing through the
            centroid of the polygon.

        Returns
        =======

        I_xx, I_yy, I_xy : number or SymPy expression
                           I_xx, I_yy are second moment of area of a two dimensional polygon.
                           I_xy is product moment of area of a two dimensional polygon.

        Examples
        ========

        >>> from sympy import Polygon, symbols
        >>> a, b = symbols('a, b')
        >>> p1, p2, p3, p4, p5 = [(0, 0), (a, 0), (a, b), (0, b), (a/3, b/3)]
        >>> rectangle = Polygon(p1, p2, p3, p4)
        >>> rectangle.second_moment_of_area()
        (a*b**3/12, a**3*b/12, 0)
        >>> rectangle.second_moment_of_area(p5)
        (a*b**3/9, a**3*b/9, a**2*b**2/36)

        References
        ==========

        .. [1] https://en.wikipedia.org/wiki/Second_moment_of_area

        """

        I_xx, I_yy, I_xy = 0, 0, 0
        args = self.vertices
        for i in range(len(args)):
            x1, y1 = args[i-1].args
            x2, y2 = args[i].args
            v = x1*y2 - x2*y1
            I_xx += (y1**2 + y1*y2 + y2**2)*v
            I_yy += (x1**2 + x1*x2 + x2**2)*v
            I_xy += (x1*y2 + 2*x1*y1 + 2*x2*y2 + x2*y1)*v
        A = self.area
        c_x = self.centroid[0]
        c_y = self.centroid[1]
        # parallel axis theorem
        I_xx_c = (I_xx/12) - (A*(c_y**2))
        I_yy_c = (I_yy/12) - (A*(c_x**2))
        I_xy_c = (I_xy/24) - (A*(c_x*c_y))
        if point is None:
            return I_xx_c, I_yy_c, I_xy_c

        I_xx = (I_xx_c + A*((point[1]-c_y)**2))
        I_yy = (I_yy_c + A*((point[0]-c_x)**2))
        I_xy = (I_xy_c + A*((point[0]-c_x)*(point[1]-c_y)))

        return I_xx, I_yy, I_xy
