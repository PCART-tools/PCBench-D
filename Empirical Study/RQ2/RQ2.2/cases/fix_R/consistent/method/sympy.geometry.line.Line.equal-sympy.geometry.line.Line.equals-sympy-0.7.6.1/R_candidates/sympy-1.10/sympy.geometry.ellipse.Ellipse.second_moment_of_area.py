    def second_moment_of_area(self, point=None):
        """Returns the second moment and product moment area of an ellipse.

        Parameters
        ==========

        point : Point, two-tuple of sympifiable objects, or None(default=None)
            point is the point about which second moment of area is to be found.
            If "point=None" it will be calculated about the axis passing through the
            centroid of the ellipse.

        Returns
        =======

        I_xx, I_yy, I_xy : number or SymPy expression
            I_xx, I_yy are second moment of area of an ellise.
            I_xy is product moment of area of an ellipse.

        Examples
        ========

        >>> from sympy import Point, Ellipse
        >>> p1 = Point(0, 0)
        >>> e1 = Ellipse(p1, 3, 1)
        >>> e1.second_moment_of_area()
        (3*pi/4, 27*pi/4, 0)

        References
        ==========

        .. [1] https://en.wikipedia.org/wiki/List_of_second_moments_of_area

        """

        I_xx = (S.Pi*(self.hradius)*(self.vradius**3))/4
        I_yy = (S.Pi*(self.hradius**3)*(self.vradius))/4
        I_xy = 0

        if point is None:
            return I_xx, I_yy, I_xy

        # parallel axis theorem
        I_xx = I_xx + self.area*((point[1] - self.center.y)**2)
        I_yy = I_yy + self.area*((point[0] - self.center.x)**2)
        I_xy = I_xy + self.area*(point[0] - self.center.x)*(point[1] - self.center.y)

        return I_xx, I_yy, I_xy
