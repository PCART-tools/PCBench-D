@_api.deprecated("3.4", alternative="MathtextBackendPath")
class MathtextBackendCairo(MathtextBackend):
    """
    Store information to write a mathtext rendering to the Cairo
    backend.
    """

    def __init__(self):
        self.glyphs = []
        self.rects = []

    def render_glyph(self, ox, oy, info):
        oy = oy - info.offset - self.height
        thetext = chr(info.num)
        self.glyphs.append(
            (info.font, info.fontsize, thetext, ox, oy))

    def render_rect_filled(self, x1, y1, x2, y2):
        self.rects.append(
            (x1, y1 - self.height, x2 - x1, y2 - y1))

    def get_results(self, box, used_characters):
        _mathtext.ship(0, 0, box)
        return (self.width,
                self.height + self.depth,
                self.depth,
                self.glyphs,
                self.rects)
