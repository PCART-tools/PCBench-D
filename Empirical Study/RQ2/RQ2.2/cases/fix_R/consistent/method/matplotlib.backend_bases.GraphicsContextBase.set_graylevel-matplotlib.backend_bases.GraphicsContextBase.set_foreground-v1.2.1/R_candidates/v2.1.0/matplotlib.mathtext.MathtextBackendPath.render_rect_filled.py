    def render_rect_filled(self, x1, y1, x2, y2):
        self.rects.append(
            (x1, self.height-y2 , x2 - x1, y2 - y1))
