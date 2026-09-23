    def render_rect_filled(self, output: Output,
                           x1: float, y1: float, x2: float, y2: float) -> None:
        """
        Draw a filled rectangle from (*x1*, *y1*) to (*x2*, *y2*).
        """
        output.rects.append((x1, y1, x2, y2))
