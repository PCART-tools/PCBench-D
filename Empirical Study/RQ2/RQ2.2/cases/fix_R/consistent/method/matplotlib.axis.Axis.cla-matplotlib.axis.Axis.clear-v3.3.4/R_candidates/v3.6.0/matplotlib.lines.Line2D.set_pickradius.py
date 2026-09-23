    @_api.rename_parameter("3.6", "d", "pickradius")
    def set_pickradius(self, pickradius):
        """
        Set the pick radius used for containment tests.

        See `.contains` for more details.

        Parameters
        ----------
        pickradius : float
            Pick radius, in points.
        """
        if not isinstance(pickradius, Number) or pickradius < 0:
            raise ValueError("pick radius should be a distance")
        self._pickradius = pickradius
