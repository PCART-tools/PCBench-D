    def _process(self):
        """Generate an event with name ``self.name`` on ``self.canvas``."""
        self.canvas.callbacks.process(self.name, self)
