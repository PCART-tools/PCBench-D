    def draw(self, drawDC=None):
        """
        Render the figure using agg.
        """
        FigureCanvasAgg.draw(self)

        self.bitmap = _convert_agg_to_wx_bitmap(self.get_renderer(), None)
        self._isDrawn = True
        self.gui_repaint(drawDC=drawDC)
