    def draw_rubberband(self, event, x0, y0, x1, y1):
        # Block copied from remove_rubberband for backend_tools convenience.
        if self.canvas._rubberband_rect_white:
            self.canvas._tkcanvas.delete(self.canvas._rubberband_rect_white)
        if self.canvas._rubberband_rect_black:
            self.canvas._tkcanvas.delete(self.canvas._rubberband_rect_black)
        height = self.canvas.figure.bbox.height
        y0 = height - y0
        y1 = height - y1
        self.canvas._rubberband_rect_black = (
            self.canvas._tkcanvas.create_rectangle(
                x0, y0, x1, y1))
        self.canvas._rubberband_rect_white = (
            self.canvas._tkcanvas.create_rectangle(
                x0, y0, x1, y1, outline='white', dash=(3, 3)))
