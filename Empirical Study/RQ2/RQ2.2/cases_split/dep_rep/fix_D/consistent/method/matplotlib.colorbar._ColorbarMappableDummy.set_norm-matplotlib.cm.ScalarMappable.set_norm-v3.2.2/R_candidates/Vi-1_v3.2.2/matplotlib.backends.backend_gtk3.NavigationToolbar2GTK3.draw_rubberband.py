    def draw_rubberband(self, event, x0, y0, x1, y1):
        # adapted from
        # http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/189744
        self.ctx = self.canvas.get_property("window").cairo_create()

        # todo: instead of redrawing the entire figure, copy the part of
        # the figure that was covered by the previous rubberband rectangle
        self.canvas.draw()

        height = self.canvas.figure.bbox.height
        y1 = height - y1
        y0 = height - y0
        w = abs(x1 - x0)
        h = abs(y1 - y0)
        rect = [int(val) for val in (min(x0, x1), min(y0, y1), w, h)]

        self.ctx.new_path()
        self.ctx.set_line_width(0.5)
        self.ctx.rectangle(rect[0], rect[1], rect[2], rect[3])
        self.ctx.set_source_rgb(0, 0, 0)
        self.ctx.stroke()
