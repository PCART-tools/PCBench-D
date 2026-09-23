    def get_ylim(self):
        """
        Return the y-axis view limits.

        Returns
        -------
        bottom, top : (float, float)
            The current y-axis limits in data coordinates.

        See Also
        --------
        .Axes.set_ylim
        .Axes.set_ybound, .Axes.get_ybound
        .Axes.invert_yaxis, .Axes.yaxis_inverted

        Notes
        -----
        The y-axis may be inverted, in which case the *bottom* value
        will be greater than the *top* value.
        """
        return tuple(self.viewLim.intervaly)
