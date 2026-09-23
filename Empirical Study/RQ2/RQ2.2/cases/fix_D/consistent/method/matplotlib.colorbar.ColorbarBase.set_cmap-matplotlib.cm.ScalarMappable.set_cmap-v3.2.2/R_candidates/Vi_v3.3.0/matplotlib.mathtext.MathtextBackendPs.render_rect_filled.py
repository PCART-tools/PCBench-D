    def render_rect_filled(self, x1, y1, x2, y2):
        ps = "%f %f %f %f rectfill\n" % (
            x1, self.height - y2, x2 - x1, y2 - y1)
        self.pswriter.write(ps)
