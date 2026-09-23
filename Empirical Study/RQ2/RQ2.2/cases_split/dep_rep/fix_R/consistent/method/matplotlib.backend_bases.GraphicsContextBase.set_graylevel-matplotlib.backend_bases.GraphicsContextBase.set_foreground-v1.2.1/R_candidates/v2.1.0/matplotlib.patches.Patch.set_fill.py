    def set_fill(self, b):
        """
        Set whether to fill the patch

        ACCEPTS: [True | False]
        """
        self._fill = bool(b)
        self._set_facecolor(self._original_facecolor)
        self._set_edgecolor(self._original_edgecolor)
        self.stale = True
