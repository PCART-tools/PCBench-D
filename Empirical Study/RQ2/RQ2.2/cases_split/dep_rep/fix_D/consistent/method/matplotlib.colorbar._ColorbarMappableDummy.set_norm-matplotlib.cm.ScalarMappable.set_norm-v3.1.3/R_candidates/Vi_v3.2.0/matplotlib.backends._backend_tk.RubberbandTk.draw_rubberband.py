    def draw_rubberband(self, x0, y0, x1, y1):
        height = self.figure.canvas.figure.bbox.height
        y0 = height - y0
        y1 = height - y1
        if hasattr(self, "lastrect"):
            self.figure.canvas._tkcanvas.delete(self.lastrect)
        self.lastrect = self.figure.canvas._tkcanvas.create_rectangle(
            x0, y0, x1, y1)
