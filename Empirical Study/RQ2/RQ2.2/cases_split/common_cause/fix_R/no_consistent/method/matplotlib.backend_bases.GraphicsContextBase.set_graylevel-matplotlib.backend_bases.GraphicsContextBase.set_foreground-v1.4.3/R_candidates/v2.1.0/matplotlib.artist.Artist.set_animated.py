    def set_animated(self, b):
        """
        Set the artist's animation state.

        ACCEPTS: [True | False]
        """
        if self._animated != b:
            self._animated = b
            self.pchanged()
