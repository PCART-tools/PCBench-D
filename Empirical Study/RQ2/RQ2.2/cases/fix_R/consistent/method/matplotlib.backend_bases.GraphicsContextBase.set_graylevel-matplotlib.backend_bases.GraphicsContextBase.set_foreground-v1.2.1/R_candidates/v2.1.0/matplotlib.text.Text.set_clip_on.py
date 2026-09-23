    def set_clip_on(self, b):
        """
        Set whether artist uses clipping.

        When False artists will be visible out side of the axes which
        can lead to unexpected results.

        ACCEPTS: [True | False]
        """
        super(Text, self).set_clip_on(b)
        self._update_clip_properties()
