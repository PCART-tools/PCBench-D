    def set_navigate(self, b):
        """
        Set whether the Axes responds to navigation toolbar commands.

        Parameters
        ----------
        b : bool

        See Also
        --------
        matplotlib.axes.Axes.set_forward_navigation_events

        """
        self._navigate = b
