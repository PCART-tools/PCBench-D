    def set_frameon(self, b):
        """
        Set whether the figure frame (background) is displayed or invisible.

        Parameters
        ----------
        b : bool
        """
        self.frameon = b
        self.stale = True
