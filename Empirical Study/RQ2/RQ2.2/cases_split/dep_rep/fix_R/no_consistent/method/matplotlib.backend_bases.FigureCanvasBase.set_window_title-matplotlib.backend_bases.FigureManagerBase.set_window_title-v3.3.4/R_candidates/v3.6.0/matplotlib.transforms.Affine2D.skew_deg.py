    def skew_deg(self, xShear, yShear):
        """
        Add a skew in place.

        *xShear* and *yShear* are the shear angles along the *x*- and
        *y*-axes, respectively, in degrees.

        Returns *self*, so this method can easily be chained with more
        calls to :meth:`rotate`, :meth:`rotate_deg`, :meth:`translate`
        and :meth:`scale`.
        """
        return self.skew(math.radians(xShear), math.radians(yShear))
