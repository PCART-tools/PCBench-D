    def draw(self, drawDC=None):
        """
        Render the figure using agg.
        """
        FigureCanvasAgg.draw(self)
        self.bitmap = self._create_bitmap()
        self._isDrawn = True
        self.gui_repaint(drawDC=drawDC)
