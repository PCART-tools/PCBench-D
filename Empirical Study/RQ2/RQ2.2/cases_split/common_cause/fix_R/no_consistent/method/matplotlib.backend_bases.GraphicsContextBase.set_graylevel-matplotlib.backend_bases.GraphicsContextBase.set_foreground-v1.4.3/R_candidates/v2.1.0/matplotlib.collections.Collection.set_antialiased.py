    def set_antialiased(self, aa):
        """
        Set the antialiasing state for rendering.

        ACCEPTS: Boolean or sequence of booleans
        """
        if aa is None:
            aa = mpl.rcParams['patch.antialiased']
        self._antialiaseds = np.atleast_1d(np.asarray(aa, bool))
        self.stale = True
