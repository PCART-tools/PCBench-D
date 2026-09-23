    def set_clip_on(self, b):
        """
        Set whether artist uses clipping.

        When False, artists will be visible outside of the axes, which can lead
        to unexpected results.

        Parameters
        ----------
        b : bool
        """
        super().set_clip_on(b)
        self._update_clip_properties()
