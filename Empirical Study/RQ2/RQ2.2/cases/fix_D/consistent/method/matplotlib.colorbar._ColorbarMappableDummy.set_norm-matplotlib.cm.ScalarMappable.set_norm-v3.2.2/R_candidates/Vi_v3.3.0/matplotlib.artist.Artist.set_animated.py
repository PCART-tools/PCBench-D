    def set_animated(self, b):
        """
        Set the artist's animation state.

        Parameters
        ----------
        b : bool
        """
        if self._animated != b:
            self._animated = b
            self.pchanged()
