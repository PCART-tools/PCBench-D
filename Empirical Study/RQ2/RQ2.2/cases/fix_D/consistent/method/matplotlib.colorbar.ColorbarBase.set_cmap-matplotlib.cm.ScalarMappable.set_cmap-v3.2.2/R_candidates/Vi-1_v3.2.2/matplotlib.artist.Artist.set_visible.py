    def set_visible(self, b):
        """
        Set the artist's visibility.

        Parameters
        ----------
        b : bool
        """
        self._visible = b
        self.pchanged()
        self.stale = True
