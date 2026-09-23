    def set_figwidth(self, val, forward=True):
        """
        Set the width of the figure in inches.

        Parameters
        ----------
        val : float
        forward : bool
        """
        self.set_size_inches(val, self.get_figheight(), forward=forward)
