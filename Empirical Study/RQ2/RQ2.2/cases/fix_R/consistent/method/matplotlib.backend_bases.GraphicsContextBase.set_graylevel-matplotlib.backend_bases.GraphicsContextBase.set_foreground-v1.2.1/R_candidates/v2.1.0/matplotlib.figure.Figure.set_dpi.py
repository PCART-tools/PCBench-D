    def set_dpi(self, val):
        """
        Set the dots-per-inch of the figure

        ACCEPTS: float
        """
        self.dpi = val
        self.stale = True
