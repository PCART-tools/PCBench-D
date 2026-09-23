    def get_xlim(self):
        """
        Return the x-axis view limits.

        Returns
        -------
        left, right : (float, float)
            The current x-axis limits in data coordinates.

        See Also
        --------
        .Axes.set_xlim
        .Axes.set_xbound, .Axes.get_xbound
        .Axes.invert_xaxis, .Axes.xaxis_inverted

        Notes
        -----
        The x-axis may be inverted, in which case the *left* value will
        be greater than the *right* value.
        """
        return tuple(self.viewLim.intervalx)
