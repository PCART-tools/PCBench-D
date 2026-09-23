    def render(self, output: Output,  # type: ignore[override]
               x: float, y: float, w: float, h: float) -> None:
        self.fontset.render_rect_filled(output, x, y, x + w, y + h)
