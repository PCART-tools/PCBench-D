    def set_figwidth(self, val, forward=True):
        """
        Set the width of the figure in inches.

        .. ACCEPTS: float
        """
        self.set_size_inches(val, self.get_figheight(), forward=forward)
