    def set_frame_on(self, b):
        """
        Set whether the legend box patch is drawn

        ACCEPTS: [ *True* | *False* ]
        """
        self._drawFrame = b
        self.stale = True
