    def set_visible(self, b):
        """
        Set the artist's visibility.

        Parameters
        ----------
        b : bool
        """
        if b != self._visible:
            self._visible = b
            self.pchanged()
            self.stale = True
