    def draw(self, drawDC=None):
        """
        Render the figure using agg.
        """
        FigureCanvasAgg.draw(self)
        self.bitmap = _rgba_to_wx_bitmap(self.get_renderer().buffer_rgba())
        self._isDrawn = True
        self.gui_repaint(drawDC=drawDC)
