@_api.deprecated("3.6")
class MathtextBackendPath(MathtextBackend):
    """
    Store information to write a mathtext rendering to the text path
    machinery.
    """

    _Result = namedtuple("_Result", "width height depth glyphs rects")

    def __init__(self):
        super().__init__()
        self.glyphs = []
        self.rects = []

    def render_glyph(self, ox, oy, info):
        oy = self.height - oy + info.offset
        self.glyphs.append((info.font, info.fontsize, info.num, ox, oy))

    def render_rect_filled(self, x1, y1, x2, y2):
        self.rects.append((x1, self.height - y2, x2 - x1, y2 - y1))

    def get_results(self, box):
        return _mathtext.ship(box).to_vector()
