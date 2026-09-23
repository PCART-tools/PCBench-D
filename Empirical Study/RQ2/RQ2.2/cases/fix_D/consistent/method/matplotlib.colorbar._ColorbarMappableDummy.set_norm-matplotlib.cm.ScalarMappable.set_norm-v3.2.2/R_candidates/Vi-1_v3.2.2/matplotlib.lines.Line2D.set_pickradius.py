    def set_pickradius(self, d):
        """Set the pick radius used for containment tests.

        See `.contains` for more details.

        Parameters
        ----------
        d : float
            Pick radius, in points.
        """
        self.pickradius = d
