    @property
    def semilatus_rectum(self):
        """
        Calculates the semi-latus rectum of the Ellipse.

        Semi-latus rectum is defined as one half of the chord through a
        focus parallel to the conic section directrix of a conic section.

        Returns
        =======

        semilatus_rectum : number

        See Also
        ========

        apoapsis : Returns greatest distance between focus and contour

        periapsis : The shortest distance between the focus and the contour

        Examples
        ========

        >>> from sympy import Point, Ellipse
        >>> p1 = Point(0, 0)
        >>> e1 = Ellipse(p1, 3, 1)
        >>> e1.semilatus_rectum
        1/3

        References
        ==========

        .. [1] http://mathworld.wolfram.com/SemilatusRectum.html
        .. [2] https://en.wikipedia.org/wiki/Ellipse#Semi-latus_rectum

        """
        return self.major * (1 - self.eccentricity ** 2)
