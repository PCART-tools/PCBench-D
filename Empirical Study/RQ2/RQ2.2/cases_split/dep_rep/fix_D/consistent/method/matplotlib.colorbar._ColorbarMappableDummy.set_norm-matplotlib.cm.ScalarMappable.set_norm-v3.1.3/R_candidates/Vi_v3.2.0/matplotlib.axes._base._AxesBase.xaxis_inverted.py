    def xaxis_inverted(self):
        """
        Return whether the x-axis is inverted.

        The axis is inverted if the left value is larger than the right value.

        See Also
        --------
        invert_xaxis
        get_xlim, set_xlim
        get_xbound, set_xbound
        """
        return self.xaxis.get_inverted()
