    def draw(self, drawDC=None):
        """
        Render the figure using RendererWx instance renderer, or using a
        previously defined renderer if none is specified.
        """
        DEBUG_MSG("draw()", 1, self)
        self.renderer = RendererWx(self.bitmap, self.figure.dpi)
        self.figure.draw(self.renderer)
        self._isDrawn = True
        self.gui_repaint(drawDC=drawDC)
