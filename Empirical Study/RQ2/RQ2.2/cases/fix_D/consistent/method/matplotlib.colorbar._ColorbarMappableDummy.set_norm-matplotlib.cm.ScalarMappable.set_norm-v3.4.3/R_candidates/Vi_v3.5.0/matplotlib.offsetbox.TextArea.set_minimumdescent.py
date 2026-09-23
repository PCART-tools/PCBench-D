    @_api.deprecated("3.4")
    def set_minimumdescent(self, t):
        """
        Set minimumdescent.

        If True, extent of the single line text is adjusted so that
        its descent is at least the one of the glyph "p".
        """
        # The current implementation of Text._get_layout always behaves as if
        # this is True.
        self._minimumdescent = t
        self.stale = True
