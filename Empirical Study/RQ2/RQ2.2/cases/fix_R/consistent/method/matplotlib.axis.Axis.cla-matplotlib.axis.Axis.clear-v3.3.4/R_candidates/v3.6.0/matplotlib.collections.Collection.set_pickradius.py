    @_api.rename_parameter("3.6", "pr", "pickradius")
    def set_pickradius(self, pickradius):
        """
        Set the pick radius used for containment tests.

        Parameters
        ----------
        pickradius : float
            Pick radius, in points.
        """
        self._pickradius = pickradius
