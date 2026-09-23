    def get_kerning(self, next):
        """
        Return the amount of kerning between this and the given
        character.  Called when characters are strung together into
        :class:`Hlist` to create :class:`Kern` nodes.
        """
        advance = self._metrics.advance - self.width
        kern = 0.
        if isinstance(next, Char):
            kern = self.font_output.get_kern(
                self.font, self.font_class, self.c, self.fontsize,
                next.font, next.font_class, next.c, next.fontsize,
                self.dpi)
        return advance + kern
