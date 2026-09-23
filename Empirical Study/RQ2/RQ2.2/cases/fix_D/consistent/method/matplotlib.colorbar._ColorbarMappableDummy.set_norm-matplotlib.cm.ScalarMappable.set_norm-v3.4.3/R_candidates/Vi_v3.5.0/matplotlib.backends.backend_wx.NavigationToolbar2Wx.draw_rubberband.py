    def draw_rubberband(self, event, x0, y0, x1, y1):
        height = self.canvas.figure.bbox.height
        self.canvas._rubberband_rect = (x0, height - y0, x1, height - y1)
        self.canvas.Refresh()
