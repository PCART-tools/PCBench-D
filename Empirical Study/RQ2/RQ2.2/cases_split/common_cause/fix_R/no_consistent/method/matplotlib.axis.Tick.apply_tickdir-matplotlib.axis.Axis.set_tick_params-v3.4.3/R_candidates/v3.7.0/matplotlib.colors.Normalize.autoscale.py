    def autoscale(self, A):
        """Set *vmin*, *vmax* to min, max of *A*."""
        with self.callbacks.blocked():
            # Pause callbacks while we are updating so we only get
            # a single update signal at the end
            self.vmin = self.vmax = None
            self.autoscale_None(A)
        self._changed()
