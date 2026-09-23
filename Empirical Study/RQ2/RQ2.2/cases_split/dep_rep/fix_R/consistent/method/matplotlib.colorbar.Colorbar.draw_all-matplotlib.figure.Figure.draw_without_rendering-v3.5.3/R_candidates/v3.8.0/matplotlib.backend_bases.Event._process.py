    def _process(self):
        """Process this event on ``self.canvas``, then unset ``guiEvent``."""
        self.canvas.callbacks.process(self.name, self)
        self._guiEvent_deleted = True
