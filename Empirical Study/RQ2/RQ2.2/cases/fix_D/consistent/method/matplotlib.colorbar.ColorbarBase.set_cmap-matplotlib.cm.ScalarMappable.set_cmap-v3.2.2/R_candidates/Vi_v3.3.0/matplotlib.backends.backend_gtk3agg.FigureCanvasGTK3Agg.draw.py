    def draw(self):
        if self.get_visible() and self.get_mapped():
            backend_agg.FigureCanvasAgg.draw(self)
        super().draw()
