    def render_rect_filled(self, output, x1, y1, x2, y2):
        """
        Draw a filled rectangle from (*x1*, *y1*) to (*x2*, *y2*).
        """
        output.rects.append((x1, y1, x2, y2))
