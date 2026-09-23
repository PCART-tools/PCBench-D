    def _draw(self):
        renderer = self.get_renderer()

        if not self.figure.stale:
            return renderer

        self.figure.draw(renderer)
        return renderer
