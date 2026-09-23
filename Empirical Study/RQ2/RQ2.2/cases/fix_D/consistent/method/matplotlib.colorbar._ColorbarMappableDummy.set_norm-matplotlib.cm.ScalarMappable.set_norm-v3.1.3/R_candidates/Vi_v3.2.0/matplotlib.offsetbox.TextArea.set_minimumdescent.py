    def set_minimumdescent(self, t):
        """
        Set minimumdescent .

        If True, extent of the single line text is adjusted so that
        it has minimum descent of "p"
        """
        self._minimumdescent = t
        self.stale = True
