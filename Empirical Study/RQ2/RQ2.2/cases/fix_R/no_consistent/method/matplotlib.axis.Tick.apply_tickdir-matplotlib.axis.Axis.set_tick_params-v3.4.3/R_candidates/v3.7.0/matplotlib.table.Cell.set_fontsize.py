    def set_fontsize(self, size):
        """Set the text fontsize."""
        self._text.set_fontsize(size)
        self.stale = True
