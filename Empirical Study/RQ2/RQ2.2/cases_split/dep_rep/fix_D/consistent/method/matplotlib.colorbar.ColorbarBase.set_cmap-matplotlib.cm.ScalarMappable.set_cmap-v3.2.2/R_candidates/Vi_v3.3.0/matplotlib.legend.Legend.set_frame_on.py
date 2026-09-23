    def set_frame_on(self, b):
        """
        Set whether the legend box patch is drawn.

        Parameters
        ----------
        b : bool
        """
        self.legendPatch.set_visible(b)
        self.stale = True
