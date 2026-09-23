    def set_pickradius(self, d):
        """
        Set the pick radius used for containment tests.

        See `.contains` for more details.

        Parameters
        ----------
        d : float
            Pick radius, in points.
        """
        if not isinstance(d, Number) or d < 0:
            raise ValueError("pick radius should be a distance")
        self._pickradius = d
