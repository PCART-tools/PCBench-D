    def set_dashdirection(self, dd):
        """
        Set the direction of the dash following the text.  1 is before the text
        and 0 is after. The default is 0, which is what you'd want for the
        typical case of ticks below and on the left of the figure.

        Parameters
        ----------
        dd : int (1 is before, 0 is after)
        """
        self._dashdirection = dd
        self.stale = True
