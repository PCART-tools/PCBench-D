    def render_rect_filled(self, x1, y1, x2, y2):
        self.svg_rects.append(
            (x1, self.height - y1 + 1, x2 - x1, y2 - y1))
