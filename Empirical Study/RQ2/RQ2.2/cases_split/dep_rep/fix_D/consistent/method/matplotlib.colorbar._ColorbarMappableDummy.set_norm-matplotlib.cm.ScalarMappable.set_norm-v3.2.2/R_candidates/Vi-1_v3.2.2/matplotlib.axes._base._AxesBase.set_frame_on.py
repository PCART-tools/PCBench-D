    def set_frame_on(self, b):
        """
        Set whether the axes rectangle patch is drawn.

        Parameters
        ----------
        b : bool
        """
        self._frameon = b
        self.stale = True
