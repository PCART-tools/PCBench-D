    def invert_yaxis(self):
        """
        Invert the y-axis.

        See Also
        --------
        yaxis_inverted
        get_ylim, set_ylim
        get_ybound, set_ybound
        """
        self.yaxis.set_inverted(not self.yaxis.get_inverted())
