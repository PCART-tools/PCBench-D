    def set_picker(self, p):
        """
        Set the event picker details for the line.

        Parameters
        ----------
        p : float or callable[[Artist, Event], tuple[bool, dict]]
            If a float, it is used as the pick radius in points.
        """
        if callable(p):
            self._contains = p
        else:
            self.set_pickradius(p)
        self._picker = p
