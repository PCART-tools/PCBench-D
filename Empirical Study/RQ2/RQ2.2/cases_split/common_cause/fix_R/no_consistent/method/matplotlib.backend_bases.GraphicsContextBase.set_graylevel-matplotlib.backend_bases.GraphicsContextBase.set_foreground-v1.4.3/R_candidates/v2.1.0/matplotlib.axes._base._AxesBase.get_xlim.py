    def get_xlim(self):
        """
        Get the x-axis range

        Returns
        -------
        xlimits : tuple
            Returns the current x-axis limits as the tuple
            (`left`, `right`).

        Notes
        -----
        The x-axis may be inverted, in which case the `left` value will
        be greater than the `right` value.

        """
        return tuple(self.viewLim.intervalx)
