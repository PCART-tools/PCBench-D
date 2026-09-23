    def set_clip_on(self, b):
        """
        Set whether artist uses clipping.

        When False artists will be visible out side of the axes which
        can lead to unexpected results.

        ACCEPTS: [True | False]
        """
        self._clipon = b
        # This may result in the callbacks being hit twice, but ensures they
        # are hit at least once
        self.pchanged()
        self.stale = True
