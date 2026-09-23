    def set_visible(self, b):
        """
        Set the artist's visiblity.

        ACCEPTS: [True | False]
        """
        self._visible = b
        self.pchanged()
        self.stale = True
