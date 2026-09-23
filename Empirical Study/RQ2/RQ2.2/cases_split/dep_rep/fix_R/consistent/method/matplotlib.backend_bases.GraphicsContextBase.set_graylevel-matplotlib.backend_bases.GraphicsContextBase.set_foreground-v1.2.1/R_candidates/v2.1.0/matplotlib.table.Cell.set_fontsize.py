    def set_fontsize(self, size):
        self._text.set_fontsize(size)
        self.stale = True
