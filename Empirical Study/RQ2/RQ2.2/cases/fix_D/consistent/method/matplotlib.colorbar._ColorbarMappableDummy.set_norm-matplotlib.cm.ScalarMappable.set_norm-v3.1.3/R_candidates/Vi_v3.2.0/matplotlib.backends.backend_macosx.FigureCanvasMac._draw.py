    def _draw(self):
        renderer = self.get_renderer(cleared=self.figure.stale)

        if self.figure.stale:
            self.figure.draw(renderer)

        return renderer
