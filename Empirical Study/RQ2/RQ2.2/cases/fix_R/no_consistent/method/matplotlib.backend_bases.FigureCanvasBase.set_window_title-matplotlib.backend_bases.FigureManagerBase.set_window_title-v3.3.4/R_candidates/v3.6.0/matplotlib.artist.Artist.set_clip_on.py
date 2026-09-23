    def set_clip_on(self, b):
        """
        Set whether the artist uses clipping.

        When False artists will be visible outside of the Axes which
        can lead to unexpected results.

        Parameters
        ----------
        b : bool
        """
        self._clipon = b
        # This may result in the callbacks being hit twice, but ensures they
        # are hit at least once
        self.pchanged()
        self.stale = True
