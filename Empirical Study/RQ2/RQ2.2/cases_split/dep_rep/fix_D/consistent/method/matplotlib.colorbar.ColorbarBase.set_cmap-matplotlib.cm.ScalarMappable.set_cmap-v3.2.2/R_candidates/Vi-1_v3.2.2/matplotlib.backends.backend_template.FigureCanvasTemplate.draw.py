    def draw(self):
        """Draw the figure using the renderer."""
        renderer = RendererTemplate(self.figure.dpi)
        self.figure.draw(renderer)
