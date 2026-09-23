    def set_figheight(self, val, forward=True):
        """
        Set the height of the figure in inches.

        Parameters
        ----------
        val : float
        forward : bool
        """
        self.set_size_inches(self.get_figwidth(), val, forward=forward)
