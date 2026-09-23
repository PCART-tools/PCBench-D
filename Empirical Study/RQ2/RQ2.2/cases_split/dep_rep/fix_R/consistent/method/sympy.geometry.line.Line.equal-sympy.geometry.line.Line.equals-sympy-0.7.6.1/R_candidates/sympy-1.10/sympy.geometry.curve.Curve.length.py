    @property
    def length(self):
        """The curve length.

        Examples
        ========

        >>> from sympy import Curve
        >>> from sympy.abc import t
        >>> Curve((t, t), (t, 0, 1)).length
        sqrt(2)

        """
        integrand = sqrt(sum(diff(func, self.limits[0])**2 for func in self.functions))
        return integrate(integrand, self.limits)
