@_api.deprecated("3.4", alternative="MathtextBackendPath")
class MathtextBackendSvg(MathtextBackend):
    """
    Store information to write a mathtext rendering to the SVG
    backend.
    """
    def __init__(self):
        super().__init__()
        self.svg_glyphs = []
        self.svg_rects = []

    def render_glyph(self, ox, oy, info):
        oy = self.height - oy + info.offset

        self.svg_glyphs.append(
            (info.font, info.fontsize, info.num, ox, oy, info.metrics))

    def render_rect_filled(self, x1, y1, x2, y2):
        self.svg_rects.append(
            (x1, self.height - y1 + 1, x2 - x1, y2 - y1))

    def get_results(self, box, used_characters):
        _mathtext.ship(0, 0, box)
        svg_elements = types.SimpleNamespace(svg_glyphs=self.svg_glyphs,
                                             svg_rects=self.svg_rects)
        return (self.width,
                self.height + self.depth,
                self.depth,
                svg_elements,
                used_characters)
