    def get_xlim(self):
        """
        Return the x-axis view limits.

        Returns
        -------
        left, right : (float, float)
            The current x-axis limits in data coordinates.

        See Also
        --------
        set_xlim
        set_xbound, get_xbound
        invert_xaxis, xaxis_inverted

        Notes
        -----
        The x-axis may be inverted, in which case the *left* value will
        be greater than the *right* value.

        """
        return tuple(self.viewLim.intervalx)
