    def set_markerfacecoloralt(self, fc):
        """
        Set the alternate marker face color.

        Parameters
        ----------
        fc : color
        """
        if fc is None:
            fc = 'auto'
        if np.any(self._markerfacecoloralt != fc):
            self.stale = True
        self._markerfacecoloralt = fc
