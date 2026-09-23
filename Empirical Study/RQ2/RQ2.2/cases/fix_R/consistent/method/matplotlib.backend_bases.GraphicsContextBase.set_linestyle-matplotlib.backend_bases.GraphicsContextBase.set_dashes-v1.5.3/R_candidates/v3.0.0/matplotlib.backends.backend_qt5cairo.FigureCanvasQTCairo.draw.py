    def draw(self):
        if hasattr(self._renderer.gc, "ctx"):
            self.figure.draw(self._renderer)
        super().draw()
