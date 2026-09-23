class RubberbandTk(backend_tools.RubberbandBase):
    def draw_rubberband(self, x0, y0, x1, y1):
        self.remove_rubberband()
        height = self.figure.canvas.figure.bbox.height
        y0 = height - y0
        y1 = height - y1
        self.lastrect = self.figure.canvas._tkcanvas.create_rectangle(
            x0, y0, x1, y1)

    def remove_rubberband(self):
        if hasattr(self, "lastrect"):
            self.figure.canvas._tkcanvas.delete(self.lastrect)
            del self.lastrect
