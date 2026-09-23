    def set_frame_on(self, b):
        """
        Set whether the axes rectangle patch is drawn

        ACCEPTS: [ *True* | *False* ]
        """
        self._frameon = b
        self.stale = True
