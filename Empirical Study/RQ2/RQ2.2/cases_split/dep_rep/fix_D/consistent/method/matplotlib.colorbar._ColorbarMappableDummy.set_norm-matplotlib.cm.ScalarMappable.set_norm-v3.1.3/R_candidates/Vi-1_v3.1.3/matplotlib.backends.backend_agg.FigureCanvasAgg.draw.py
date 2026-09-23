    def draw(self):
        """
        Draw the figure using the renderer.
        """
        self.renderer = self.get_renderer(cleared=True)
        with RendererAgg.lock:
            self.figure.draw(self.renderer)
            # A GUI class may be need to update a window using this draw, so
            # don't forget to call the superclass.
            super().draw()
