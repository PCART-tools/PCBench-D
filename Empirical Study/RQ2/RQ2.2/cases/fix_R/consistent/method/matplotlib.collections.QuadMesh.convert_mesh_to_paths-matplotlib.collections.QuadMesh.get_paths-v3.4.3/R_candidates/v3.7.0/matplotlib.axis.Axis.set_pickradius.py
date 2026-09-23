    def set_pickradius(self, pickradius):
        """
        Set the depth of the axis used by the picker.

        Parameters
        ----------
        pickradius : float
            The acceptance radius for containment tests.
            See also `.Axis.contains`.
        """
        if not isinstance(pickradius, Number) or pickradius < 0:
            raise ValueError("pick radius should be a distance")
        self._pickradius = pickradius
