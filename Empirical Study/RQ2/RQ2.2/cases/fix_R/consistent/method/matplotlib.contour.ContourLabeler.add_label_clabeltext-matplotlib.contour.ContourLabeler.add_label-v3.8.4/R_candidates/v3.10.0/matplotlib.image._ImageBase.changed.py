    def changed(self):
        """
        Call this whenever the mappable is changed so observers can update.
        """
        self._imcache = None
        super().changed()
