class MathtextBackendPath(MathtextBackend):
    """
    Store information to write a mathtext rendering to the text path
    machinery.
    """

    _Result = namedtuple("_Result", "width height depth glyphs rects")

    def __init__(self):
        self.glyphs = []
        self.rects = []

    def render_glyph(self, ox, oy, info):
        oy = self.height - oy + info.offset
        self.glyphs.append((info.font, info.fontsize, info.num, ox, oy))

    def render_rect_filled(self, x1, y1, x2, y2):
        self.rects.append((x1, self.height - y2, x2 - x1, y2 - y1))

    def get_results(self, box, used_characters):
        _mathtext.ship(0, 0, box)
        return self._Result(self.width,
                            self.height + self.depth,
                            self.depth,
                            self.glyphs,
                            self.rects)
