    def get_ylim(self):
        """
        Get the y-axis range

        Returns
        -------
        ylimits : tuple
            Returns the current y-axis limits as the tuple
            (`bottom`, `top`).

        Notes
        -----
        The y-axis may be inverted, in which case the `bottom` value
        will be greater than the `top` value.

        """
        return tuple(self.viewLim.intervaly)
