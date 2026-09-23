    def set_transform(self, t):
        """
        Set the artist transform.

        Parameters
        ----------
        t : `.Transform`
        """
        self._transform = t
        self._transformSet = True
        self.pchanged()
        self.stale = True
