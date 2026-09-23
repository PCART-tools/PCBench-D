    def yaxis_inverted(self):
        """
        Return whether the y-axis is inverted.

        The axis is inverted if the bottom value is larger than the top value.

        See Also
        --------
        invert_yaxis
        get_ylim, set_ylim
        get_ybound, set_ybound
        """
        return self.yaxis.get_inverted()
